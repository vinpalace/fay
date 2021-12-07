echo "Starting fay server $FAY_PROJECT_PATH"
gnome-terminal --tab --title="Fay BE" -- zsh -l -c "cd $FAY_PROJECT_PATH; workon fay; python app.py;"
gnome-terminal --tab --title="ngrok" -- zsh -l -c "cd $FAY_PROJECT_PATH; workon fay; ngrok http 3050"
google-chrome https://api.slack.com/apps/A024PTEAXDZ/event-subscriptions?

