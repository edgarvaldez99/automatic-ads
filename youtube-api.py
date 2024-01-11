import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Credenciales de autenticación
creds = None

# El archivo JSON con las credenciales obtenido en la Consola de Desarrolladores de Google

BASE_DIR = os.path.dirname(__file__)
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "credentials", "creds.json")
# These OAuth 2.0 access scopes allow for read-only access to the authenticated
# user's account for both YouTube Data API resources and YouTube Analytics Data.
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
]
API_SERVICE_NAME = "youtubereporting"
API_VERSION = "v1"


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# Remove keyword arguments that are not set.
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


# Call the YouTube Reporting API's reportTypes.list method to retrieve report types.
def list_report_types(youtube_reporting, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)
    results = youtube_reporting.reportTypes().list(**kwargs).execute()
    reportTypes = results["reportTypes"]

    if "reportTypes" in results and results["reportTypes"]:
        reportTypes = results["reportTypes"]
        for reportType in reportTypes:
            print(
                "Report type id: %s\n name: %s\n"
                % (reportType["id"], reportType["name"])
            )
        return reportTypes[0]["id"]
    else:
        print("No report types found")
        return False


# Call the YouTube Reporting API's jobs.create method to create a job.
def create_reporting_job(youtube_reporting, report_type_id, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)

    reporting_job = (
        youtube_reporting.jobs()
        .create(body=dict(reportTypeId=report_type_id, name="job1"), **kwargs)
        .execute()
    )

    print(
        'Reporting job "%s" created for reporting type "%s" at "%s"'
        % (
            reporting_job["name"],
            reporting_job["reportTypeId"],
            reporting_job["createTime"],
        )
    )
    print(f"reporting_job={reporting_job}")


if __name__ == "__main__":
    youtube_reporting = get_authenticated_service()
    report_type_id = list_report_types(youtube_reporting)
    if report_type_id:
        print(f"report_type_id={report_type_id}")
        reporting_job = create_reporting_job(youtube_reporting, report_type_id)
