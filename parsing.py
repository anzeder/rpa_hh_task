
from enum import unique
from requests_html import HTMLSession
from bs4 import BeautifulSoup


def find_vacancy_data(item, attrs,  strip=False):
    try:
        res = item.find(attrs=attrs)
        res = res.get_text(strip=strip)
    except:
        res = None
    return res


def get_response(url, render=True):
    session = HTMLSession()
    response = session.get(url)
    if render == True:
        response.html.render(timeout=20)
    response.close()
    return response


def get_next_page(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        url = 'https://hh.kz/' + soup.find('a', attrs={
            'data-qa': 'pager-next'
        })['href']
    except:
        url = None
    return url


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='vacancy-serp-item')
    jobs = []
    unique_companies = {}

    counter = 0

    for item in items:
        counter += 1

        title = find_vacancy_data(
            item, attrs={
                'data-qa': 'vacancy-serp__vacancy-title'
            },
            strip=True
        )

        salary = find_vacancy_data(
            item, attrs={
                'data-qa': 'vacancy-serp__vacancy-compensation'
            })
        if salary != None:

            salary = salary.replace(u"\u202f", " ")
            salary = salary.strip()

        is_remote = find_vacancy_data(
            item,
            attrs={
                'data-qa': 'vacancy-serp__vacancy-work-schedule'
            })

        is_trusted = find_vacancy_data(
            item, attrs={
                'class': 'vacancy-serp-bage-trusted-employer'
            })

        is_hr_brand = find_vacancy_data(
            item, attrs={
                'class': 'vacancy-serp-bage-hr-brand'
            })

        is_resume = find_vacancy_data(
            item,
            attrs={
                'class': 'search-result-label search-result-label_no-resume'
            })

        href = item.find(
            attrs={'data-qa': "vacancy-serp__vacancy-title"})['href']
        detailed_vacancy = get_response(href, render=False)

        soup = BeautifulSoup(detailed_vacancy.text, 'html.parser')

        experience = find_vacancy_data(
            soup, attrs={
                'data-qa': "vacancy-experience"
            }, strip=True
        )

        employ_mode = find_vacancy_data(
            soup, attrs={
                'data-qa': "vacancy-view-employment-mode"
            }, strip=True
        )

        full_address = find_vacancy_data(
            soup, attrs={
                'data-qa': 'vacancy-view-raw-address'
            }, strip=True
        )

        temp_options = find_vacancy_data(
            soup, attrs={
                'data-qa': "vacancy-view-accept-temporary"
            }, strip=True
        )

        parttime_options = find_vacancy_data(
            soup, attrs={
                'data-qa': "vacancy-view-parttime-options"
            }, strip=True
        )
        if parttime_options != None:
            parttime_options = parttime_options.replace('\xa0', ' ')
            parttime_options = parttime_options.strip()

        company = find_vacancy_data(
            item, attrs={
                'data-qa': 'vacancy-serp__vacancy-employer'
            })
        if company != None:
            company = company.replace('\xa0', ' ')
            company = company.strip()

            unique_companies[company] = {
                'is_trusted': True if is_trusted != None else False,
                'is_hr_brand': True if is_hr_brand != None else False
            }

        jobs.append({
            'title': title,
            'employ_mode': employ_mode,
            'experience': experience,
            'parttime_options': parttime_options,
            'temp_options': temp_options,
            'company_title': company,
            'full_address': full_address,
            'salary': salary,
            'is_remote': True if is_remote != None else False,
            'is_trusted': True if is_trusted != None else False,
            'is_hr_brand': True if is_hr_brand != None else False,
            'is_resume': True if is_resume == None else False
        })
        b = "Loaded " + str(counter) + " item(s) out of " + str(len(items))
        print(b, end="\r")
    print()
    return jobs, unique_companies


def txt_writer(jobs, unique_companies):
    with open('parsed.txt', 'w',  encoding="utf-8") as f:
        s = ''
        counter = 0
        for job in jobs:
            s += '\n-------------------\n\n'
            s += 'id(' + str(counter) + ') ' + job['title'] + '\n'
            s += 'id(' + str(list(unique_companies.keys()).index(job['company_title'])) + ') ' + job['company_title'] + \
                '\n' + \
                (job['full_address'] if job['full_address'] != None else 'Алматы   ') +  \
                '\n'

            s += job['salary'] if job['salary'] != None else 'No Salary'
            s += '\n'

            s += 'Remote job' if job['is_remote'] == True else 'Not remote'
            s += '\n'

            s += 'Trusted Employer' if unique_companies[job['company_title']
                                                        ]['is_trusted'] == True else 'Not trusted Employer'
            s += '\n'

            s += 'HR brand' if unique_companies[
                job['company_title']
            ]['is_hr_brand'] == True else 'not hr'
            s += '\n'

            s += 'Resume needed' if job['is_resume'] == True else 'No Resume'
            s += '\n'

            s += job['experience'] if job['experience'] != None else 'No Exp'
            s += '\n'

            s += job['employ_mode'] if job['employ_mode'] != None else 'No Employ'
            s += '\n'

            s += job['parttime_options'] if job['parttime_options'] != None else 'No Part'
            s += '\n'

            s += job['temp_options'] if job['temp_options'] != None else 'No Temp'
            s += '\n'

            s += '\n-------------------\n'
            counter += 1

        f.write(s)
        print('Done')
