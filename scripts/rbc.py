import urllib.request
import json
import re
import os

# test url = "https://jobs.rbc.com/ca/en/job/R-0000048184/Senior-Data-Engineer"
def scrape_rbc(url):

    desc_cleaned = ""
    job_url = ""
    job_title = ""
    job_id = ""
    application_deadline = ""

    occupationalCategory = ""
    responsibilities = ""
    skills = ""
    hiringOrganization = ""

    # Retrieve the JSON data from the URL
    with urllib.request.urlopen(url) as url_response:
        data = url_response.read().decode()
        regex = '<script type="application\/ld\+json">(.*?)<\/script>'

        try:
            match = re.findall(regex, data)[0]
        except:
            print("data not found!")

        if match:
            # Use non-greedy regex to remove html tags
            desc_cleaned = re.sub(r'&lt;.*?&gt;', ' ', match)
            application_deadline = re.findall("Application Deadline:.*?(\d{4}-\d{2}-\d{2})", desc_cleaned)[0]
            # print(cleaned_desc[600:1200])

            # Transform into JSON object
            json_desc = json.loads(desc_cleaned)
            job_url = json_desc.keys()

            job_url = json_desc['hiringOrganization']['url']
            job_title = json_desc['title']
            job_id = json_desc['identifier']['value']    
            occupationalCategory = json_desc['occupationalCategory']    
            responsibilities = json_desc['responsibilities']    
            skills = json_desc['skills'] 
            hiringOrganization = json_desc['hiringOrganization']['name']   

            # print(job_url)
            # print(job_title, job_id)
            # print(type(json_desc['description']))
            # print(json_desc['description'])
            # print(application_deadline)

    # Create the organization's folder if not exist
    folder_path = f"output/{hiringOrganization}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # create a file for the job description
    fh = f"{folder_path}/{application_deadline} {job_title} {job_id}.txt"
    try:
        with open(fh, "w") as outfile:
            outfile.write("job_id: " + job_id + "\n\n")
            outfile.write("job_url: " + job_url + "\n\n")
            outfile.write("job_title: " + job_title + "\n\n")
            outfile.write("application_deadline: " + application_deadline + "\n\n")
            outfile.write("occupationalCategory: " + occupationalCategory + "\n\n")
            outfile.write("responsibilities: " + responsibilities + "\n\n")
            outfile.write("skills: " + skills + "\n\n")
    except Exception as e:
        print("Error creating an output file:\n" + e)

    print("File created")

if __name__ == "__main__":
    scrape_rbc()