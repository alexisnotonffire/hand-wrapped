# Hand Wrapped
Handwrapped provides a tool to put your Spotify history into a GCP project, with failure alerts heading to an IFTTT endpoint. Also populates a PubSub topic so the data can be used in other projects. Needs to be scheduled to run via cron or WTS.

# Setup
Before doing anything you must setup a GCP project and Spotify app. You'll also need to allow inbound HTTP requests on port 9898 through your router and firewall. All of these are beyond the scope of this setup guide.

After doing that, you'll also need to head to your GCP project and create a PubSub topic and subscription, and a BigQuery dataset and Table. This project is hardcoded for EU datasets only (sorry, I'm an idiot). The table does not need a schema as we're using autodetect.

The first time you run this you must be using a device with a GUI based browser. This will allow you to approve Spotify's confirmation request granting access to the application.

#### Get ```config.yaml``` sorted
Begin by opening up the ```config.yaml``` file. Here, replace the comments with your own values based on how you described your App and Project to Spotify and Google respectively. The ```alert``` value is an option IFTTT webhook that will receive notifications of failed runs.

After that, open the terminal, navigate to ```*/GiftWrapped/HandWrapped``` and run
```
python main.py
```
This will open a browser for you to confirm the request and should redirect you to a page where you'll see a URI that looks like
```
https://redirect_uri?code=THIS-IS-WHAT-YOU-NEED
```
Take this value and copy it into ```config.yaml``` under ```code```. Then kill the process.

#### Sorted!
After doing the above, run
```
python main.py
```
again and it will finish populating ```config.yaml```, your PubSub topic and your Table.

Now schedule that command to run every 10 minutes or so.

# Next Steps
This project is very much early days and while it currently 'works', it could be much better. Upcoming features and fixes include:
- [ ] Better filtering with after as current version may miss tracks
- [ ] Visualise history data, ala Giftwrapped
- [ ] Automate entire process
- [ ] Populate full track data
- [ ] Populate playlists based on new listens
