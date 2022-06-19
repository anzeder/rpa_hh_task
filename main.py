from numpy import append
import parsing
import hh_db as db


if __name__ == "__main__":
    url = 'https://hh.kz/search/vacancy?area=160&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&hhtmFrom=vacancy_search_list'
    all_jobs = []
    all_companies = {}
    counter_pages = 0
    unique_companies = []
    while True:

        counter_pages += 1
        response = parsing.get_response(url, render=True)

        print("Starting to parse the page #", counter_pages)

        jobs, companies = parsing.parse(response.html.raw_html)
        all_jobs.extend(jobs)
        all_companies.update(companies)
        url = parsing.get_next_page(response.html.raw_html)

        if url == None:
            break

    parsing.txt_writer(all_jobs, all_companies)
    db.create_database()
    db.insert_companies(all_companies)
    db.select_companies()
    db.insert_jobs(all_jobs, all_companies)
    db.select_jobs()
    db.close_connection()
