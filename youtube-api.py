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
    # "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
]
API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def run_analytics_report(youtube_analytics, **kwargs):
  # Call the Analytics API to retrieve a report. Pass args in as keyword
  # arguments to set values for the following parameters:
  #
  #   * ids
  #   * metrics
  #   * dimensions
  #   * filters
  #   * start_date
  #   * end_date
  #   * sort
  #   * max_results
  #
  # For a list of available reports, see:
  # https://developers.google.com/youtube/analytics/v1/channel_reports
  # https://developers.google.com/youtube/analytics/v1/content_owner_reports
  analytics_query_response = youtube_analytics.reports().query(
    **kwargs
  ).execute()

  for column_header in analytics_query_response.get('columnHeaders', []):
    print(f"{column_header['name']}"),
  print(" ")

  for row in analytics_query_response.get('rows', []):
    for value in row:
      print(f"{value}"),
    print(" ")


if __name__ == "__main__":
    youtube_reporting = get_authenticated_service()
    run_analytics_report(
       youtube_reporting,
       ids="channel==MINE",
       startDate="2024-01-01",
       endDate="2024-01-25",
       metrics="views,likes,estimatedMinutesWatched,averageViewDuration,subscribersGained",
       dimensions="day",
       sort="day",
    )
