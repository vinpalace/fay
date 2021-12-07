import os

from slack_bolt import App
from pprint import pprint
from subprocess import PIPE, run
import pdb
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    print(message)
    say(f"Hey there <@{message['user']}>!")


# @app.message("hey")
# def message_hello2(message, say):

#     blocks = [
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
#             }
#         },
#         {
#             "type": "actions",
#             "elements": [
#                 {
#                     "type": "button",
#                     "text": {
#                         "type": "plain_text",
#                         "emoji": True,
#                         "text": "Yes Merge it"
#                     },
#                     "style": "primary",
#                     "value": "approve_button",
#                     "action_id": "approve_button"
#                 },

#             ]
#         }
#     ]
#     say(blocks=blocks, text=f"Hey there <@{message['user']}>!")

# helper


def create_approved_block(pr):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Approved {pr} :thumb_parrot: Shall I merge it as well?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Squash and Merge"
                    },
                    "style": "primary",
                    "value": f"squash-{pr}",
                    "action_id": "approve_button"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Close PR"
                    },
                    "style": "danger",
                    "value": f"squash-{pr}",
                    "action_id": "close_pr"
                },

            ]
        }
    ]


@app.action("approve_button")
def approve_request(body, ack, say):

    # Acknowledge action request
    print(body)

    value = body['actions'][0]['value']

    subcommand, merge_url = value.split('-')
    print('mu', subcommand, merge_url)

    command = f"gh pr merge {merge_url} -s"
    ack()
    result = run(command, stdout=PIPE, stderr=PIPE,
                 universal_newlines=True, shell=True)

    if result.returncode == 0:
        # say(f"Approved {url} :thumb_parrot:")
        say(f"Merge successful for {merge_url} :merged_parrot:")
    elif result.stderr:
        say(result.stderr)


@app.action("close_pr")
def approve_request(body, ack, say):

    # Acknowledge action request
    print(body)

    value = body['actions'][0]['value']

    subcommand, merge_url = value.split('-')
    print('mu', subcommand, merge_url)

    command = f"gh pr close {merge_url}"
    ack()
    result = run(command, stdout=PIPE, stderr=PIPE,
                 universal_newlines=True, shell=True)

    if result.returncode == 0:
        # say(f"Approved {url} :thumb_parrot:")
        say(
            f"PR has been closed :x: :sad_parrot:")
    elif result.stderr:
        say(result.stderr)


def get_urls(message):
    urls = []
    elements = message['blocks'][0]['elements'][0]['elements']
    for element in elements:
        if element['type'] == 'link':
            urls.append(element['url'])
    return urls


def validate_pr_url(url):
    # return True
    return "https://github.com/FSSPayfac/portal/pull/" in url


@ app.message("approve PR")
@ app.message("approve pr")
@ app.message("accept pr")
@ app.message("accept PR")
@ app.message("approve")
@ app.message("Approve")
def approve_pr(message, say):
    pprint(message)
    urls = get_urls(message)
    for url in urls:
        if validate_pr_url(url):
            blocks = create_approved_block(url)
            command = f"gh pr review {url} --approve"

            result = run(command, stdout=PIPE, stderr=PIPE,
                         universal_newlines=True, shell=True)

            if result.returncode == 0:
                # say(f"Approved {url} :thumb_parrot:")
                say(blocks=blocks, text="success")
            elif result.stderr:
                say(result.stderr)

        else:
            say(
                f"can only approve PRs for https://github.com/FSSPayfac/portal/pull/ instead got {url}")


@app.message("standup")
@app.message("Standup")
def announce_standup(message, say):
    say("Standup Link - https://meet.google.com/icq-atfw-ssu")


@app.message("meeting room 1")
def announce_meetingroom_1(message, say):
    say("Meeting Room 1 - https://meet.google.com/gmg-evyr-ypm")


@app.message("meeting room 2")
def announce_meetingroom_2(message, say):
    say("Meeting Room 2 - https://meet.google.com/cse-tvfs-tsk")


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


# @app.event("hello")
# def startup(event, say):
#     command = "gh --version"
#     result = run(command, stdout=PIPE, stderr=PIPE,
#                  universal_newlines=True, shell=True)
#     say(f"Connected successfully to Github - {result}")


@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3050)))
