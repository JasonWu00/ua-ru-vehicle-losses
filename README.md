# On Russia's invasion of Ukraine

When was the last time you thought about the war[^1] in Ukraine?

Have you, between 24 February 2022 and now, seen or heard any of these statements?
* The Kyiv offensive is a feint
* The Kharkiv / Kherson battles are futile gestures, Russia has lost nothing at all
* Russia has destroyed 60 HIMARS (or some other large number of Western equipment)

If you have heard or seen one or more of these statements, or other similar statements, and want to know if any of them are legitimate, keep reading.

### Project Description

This project uses publicly available data sets on Russia's invasion of Ukraine, most notably the [Oryx blog](https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html), to derive correlations and make conclusions on the state of the conflict.

Our project is deployed onto Streamlit. [Click this link to access the Streamlit app.](https://ua-ru-vehicle-losses.streamlit.app)

Note that the Streamlit app might go inactive if it is left idle for a long time. If the app is down, you can reach out to the owner of this repository to request it to be put back up.

Our project touches upon the following topics:
* The distribution of visually confirmed lost vehicles, for both sides, from the start of the war to recently
* The state of the vehicles lost (judged using their years of production)
* The effects of donated vehicles on the war
* The effects of the war on Ukraine's civilian population

### Technologies

This project uses the following languages, technologies, and libraries:

For scraping and processing the data sets (as we did [here](https://github.com/JasonWu00/ua-ru-losses-scraper/)):
* Python
  * BeautifulSoup
  * Requests
  * HuggingFace (pre-trained models)
  * Python Notebooks
* Google Colab (for running the HuggingFace models)[^2]

For rendering the final work:
* Python
  * Pandas
  * Plotly
  * Streamlit
  * Matplotlib

### Running the Project Locally

To run the project locally, follow these steps:

1. Ensure that you have git and Python (3.10) installed. Open your terminal and enter into it `python --version` and `git -v`.
2. Make a copy of this repo. You may download the repo as a .zip then unzip to a folder of your choice, or you may choose to navigate to a folder of your choice with your command console and type `git clone https://github.com/CTP-DS-335/DS-project.git`.
3. Install all required libraries: enter `pip install -r requirements.txt`.
4. Run the presentation locally: enter `streamlit run 0-Homepage.py`.

### Contributions

If you notice an problem with our work but do not have the know-how to implement a solution, [create an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) detailing the problem and we will get to it. If you wish to fix the problem, create a branch, implement your solution there, then open a Pull Request (PR) detailing your solution.

Steps to create a Pull Request:
1. Create a fork of this repo using the GitHub website.
2. Clone your fork onto your local device: `git clone git@github.com:YourUsername/YourForkName.git`
3. Implement your changes to this fork. We assume that you know how to use `git commit` and `git push`.
4. Commit and push your changes: `git commit -m "custom commit message here"`.
5. Open a Pull Request from the GitHub website.
  * Remember to describe in the PR what your solution entails.

### Other notes

The `data/oryx` CSV files are derived using Python scripts from [this repo](https://github.com/JasonWu00/ua-ru-losses-scraper/).

[^1]: Contrary to what some might claim, this conflict is far more than a "special military operation".

[^2]: Due to hardware limitations, we had to run some of our code on a Google Colab instance.
