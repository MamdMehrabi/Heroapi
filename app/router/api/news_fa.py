from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import httpx
import re

client = httpx.AsyncClient()

router = APIRouter(tags=["News"])


def beautifulsoup_instance(html_data: str, features: str = "html.parser"):
    return BeautifulSoup(markup=html_data, features=features)


@router.get("/news/v1", status_code=status.HTTP_200_OK)
@router.post("/news/v1", status_code=status.HTTP_200_OK)
async def news(response: Response, page: Optional[int] = 1) -> dict:
    """
    Web service to display news. onnected to the site www.tasnimnews.com
    """
    url = "https://www.tasnimnews.com"
    request = await client.request("GET", f"{url}/fa/top-stories?page={page}")
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    soup = beautifulsoup_instance(request.text, "html.parser")
    articles = soup.find_all("article", class_="list-item")

    search_result = list()
    for article in articles:
        title = article.find("h2", class_="title").text.strip()
        description = article.find("h4").text.strip()
        image = article.find("img", src=True)
        full_url = article.find("a", href=True)
        search_result.append(
            dict(
                title=title,
                description=description,
                url=url + full_url["href"],
                image=image["src"]
            )
        )

    return {
        "success": True,
        "data": search_result,
        "error_message": None
    }


@router.get("/news/v2", status_code=status.HTTP_200_OK)
@router.post("/news/v2", status_code=status.HTTP_200_OK)
async def news_version_two(response: Response, page: Optional[int] = 1) -> dict:
    """
    Web service, the latest technological news. `page` parameter has 6000 pages
    """
    request = await client.request("GET", f"https://gadgetnews.net/page/{page}")
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    soup = beautifulsoup_instance(request.text, "html.parser")

    final_values = list()
    for recent_post in range(0, 13):
        articles = soup.find_all("article", class_=f"item-list recent-post{recent_post} recent-post-blog")
        for article in articles:
            post_box = article.find("h2", class_="post-box-title")
            bookmark_post = post_box.find("a", rel="bookmark", href=True)
            post_url, post_title = bookmark_post.get("href"), bookmark_post.text

            post_meta = article.find("p", class_="post-meta")
            post_author_data = post_meta.find("span", class_="post-meta-author")
            post_author_link = post_author_data.find("a", href=True).get("href")
            post_author_name = post_author_data.find("a", href=True).text

            post_date = post_meta.find("span", class_="tie-date").text

            post_thumbnail_data = article.find("div", class_="post-thumbnail")
            post_image_data = post_thumbnail_data.find("img", decoding="async", src=True).get("srcset")
            post_images = re.findall(r"(https:\/\/.*?\.jpg)", post_image_data)

            entry_article = article.find("div", class_="entry")
            paragraph = entry_article.find("p").text

            final_values.append(
                dict(
                    post_url=post_url,
                    post_title=post_title,
                    paragraph=paragraph,
                    author=dict(
                        author_link=post_author_link, name=post_author_name
                    ),
                    date=post_date,
                    images=post_images
                )
            )

    return {
        "success": True,
        "data": final_values,
        "error_message": None
    }
