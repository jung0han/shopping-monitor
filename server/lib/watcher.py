import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, date
from lib.bot import echo

from models import Comments, Posts, Views

KEYWORDS = ["피자", "펩시", " "]
MESSAGE = {"ppomppu": "%s\nhttps://m.ppomppu.co.kr/new/bbs_view.php?id=ppomppu&no=%s"}


async def ppomppu(db):
    url = "https://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu"
    response = requests.get(url)
    p_id = re.compile("no=([0-9]+)")
    p_time = re.compile("\\d\\d:\\d\\d:\\d\\d")

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        subjects = soup.select(".bbsList_new > li > a")

        for subject in subjects:
            link = subject["href"]
            ppomppu_id = p_id.findall(link)[0]  # type: ignore
            ppomppu = db.query(Posts).get(int(ppomppu_id))

            if ppomppu is None:
                span_cont = subject.find("span", attrs={"class": "cont"})
                title = span_cont.text if span_cont else ""

                time_tag = subject.time
                date_or_time = time_tag.text if time_tag else "00:00:00"
                time_or_none = p_time.findall(date_or_time)
                date_string = "%sT%s" % (
                    date.today().isoformat(),
                    time_or_none[0] if time_or_none else "00:00:00",
                )
                created_at = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")

                ppomppu = Posts(
                    id=ppomppu_id,
                    board="ppomppu",
                    title=title.strip(),
                    created_at=created_at,
                )
                db.add(ppomppu)

                if any(x in title for x in KEYWORDS):
                    await echo(MESSAGE["ppomppu"] % (title, ppomppu_id))

            span_rp = subject.find("span", attrs={"class": "rp"})
            comments_count = int(span_rp.text) if span_rp else 0
            comment = Comments(count=int(comments_count), ppomppu_id=ppomppu_id)

            span_view = subject.find("span", attrs={"class": "view"})
            views_count = int(span_view.text) if span_view else 0
            view = Views(count=int(views_count), ppomppu_id=ppomppu_id)

            db.add(comment)
            db.add(view)

            try:
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
