from requests_html import HTMLSession
import json
import time


class Reviews:
    def __inti__(self, asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        self.url = f'https://www.amazon.de/product-reviews/{self.asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='


    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        if not r.html.find('div[´data-hook=review]'):
            return False
        else:
            return r.html.find('div[´data-hook=review]')

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook=review-title', first=True).text
            rating = review.find('i[data-hook=review-star-rating] span', first=True).text
            body = review.find('span[data-hook=review-star-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'title': title,
                'rating': rating,
                'body': body[:100]
            }
            total.append(data)
        return total

    def save(self, results):
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dumps(results, f)

if __name__ == '__main__':
    amz = Reviews('GF3FUOOZH8')
    results = []
    for x in range(1,5):
        print('getting page ', x)
        time.sleep(0.3)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.append(amz.parse(reviews))
        else:
            print('no more pages')
            break
    amz.save(results)
