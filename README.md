# xtream AI Challenge

## Ready Player 1? 🚀

Hey there! If you're reading this, you've already aced our first screening. Awesome job! 👏👏👏

Welcome to the next level of your journey towards the [xtream](https://xtreamers.io) AI squad. Here's your cool new assignment.

Take your time – you've got **10 days** to show us your magic, starting from when you get this. No rush, work at your pace. If you need more time, just let us know. We're here to help you succeed. 🤝

### What You Need to Do

Think of this as a real-world project. Fork this repo and treat it as if you're working on something big! When the deadline hits, we'll be excited to check out your work. No need to tell us you're done – we'll know. 😎

🚨 **Heads Up**: You might think the tasks are a bit open-ended or the instructions aren't super detailed. That’s intentional! We want to see how you creatively make the most out of the data and craft your own effective solutions.

🚨 **Remember**: At the end of this doc, there's a "How to run" section left blank just for you. Please fill it in with instructions on how to run your code.

### How We'll Evaluate Your Work

We'll be looking at a bunch of things to see how awesome your work is, like:

* Your approach and method
* Your understanding of the data
* The clarity and completeness of your findings
* How you use your tools (like git and Python packages)
* The neatness of your code
* The readability and maintainability of your code
* The clarity of your documentation

🚨 **Keep This in Mind**: This isn't about building the fanciest model: we're more interested in your process and thinking.

---

### Diamonds

**Problem type**: Regression

**Dataset description**: [Diamonds Readme](./datasets/diamonds/README.md)

Meet Don Francesco, the mystery-shrouded, fabulously wealthy owner of a jewelry empire. 

He's got an impressive collection of 5000 diamonds and a temperament to match - so let's keep him smiling, shall we? 
In our dataset, you'll find all the glittery details of these gems, from size to sparkle, along with their values 
appraised by an expert. You can assume that the expert's valuations are in line with the real market value of the stones.

#### Challenge 1

Plot twist! The expert who priced these gems has now vanished. 
Francesco needs you to be the new diamond evaluator. 
He's looking for a **model that predicts a gem's worth based on its characteristics**. 
And, because Francesco's clientele is as demanding as he is, he wants the why behind every price tag. 

Create a Jupyter notebook where you develop and evaluate your model.

#### Challenge 2

Good news! Francesco is impressed with the performance of your model. 
Now, he's ready to hire a new expert and expand his diamond database. 

**Develop an automated pipeline** that trains your model with fresh data, 
keeping it as sharp as the diamonds it assesses.

#### Challenge 3

Finally, Francesco wants to bring your brilliance to his business's fingertips. 

**Build a REST API** to integrate your model into a web app, 
making it a cinch for his team to use. 
Keep it developer-friendly – after all, not everyone speaks 'data scientist'!

#### Challenge 4

Your model is doing great, and Francesco wants to make even more money.

The next step is exposing the model to other businesses, but this calls for an upgrade in the training and serving infrastructure.
Using your favorite cloud provider, either AWS, GCP, or Azure, design cloud-based training and serving pipelines.
You should not implement the solution, but you should provide a **detailed explanation** of the architecture and the services you would use, motivating your choices.

So, ready to add some sparkle to this challenge? Let's make these diamonds shine! 🌟💎✨

---

## How to run

Create a venv with the provided requirements.txt

#### Challenge 1
The solution is provided in the ***eda.ipynb*** notebook You can explore the notebook by running all the cells if necessary. The "best model" is already provided in the repo (maybe not the best practice but it's very small). 

#### Challenge 2
The solution is provided in the ***script_retraining.py*** file. This file enables to retrain (or train from scratch) the catboost model I studied in the first step. To test it, from terminal, go to the repo-folder xtream-ai-assignment-engineer and run the following command:
```
python3 script_retraining.py\
    --model "best_model"\
    --iterations 1000\
    --max_depth 10\
    --data "./datasets/diamonds/diamonds.csv"\
    --output_location "model_test"\
    --learning_rate 0.01
```
where the parameters are:
- model: specify the path to the model you want to continue the traing from. If a model is not specified, then a new model from scratch is trained.
- iterations: number of iterations.
- max_depth: tree max depth.
- data: specify the path to the data you wanna train the model.
- output_location: specify where to save the model, if not specified it will be automatically saved under ***model_{k}***.
- learning_rate: specify the learning rate.
#### Challenge 3
From terminal, go to the repo-folder xtream-ai-assignment-engineer and run the command "python3 app.py" (alternatively it could be python instead of python3). The output should say the server is "Running on http://127.0.0.1:5000". 
Then you can test the predict API on Postman. If necessary download it, choose a **POST** request and insert the url http://127.0.0.1:5000/predict. Then add a new Header with the key **Content-Type** and the value **application/json**. Then go to **Body** and insert the data as:
- dictionary (with the proper keys specified below) if only one instance to predict, for instance:
```json
    {
        "carat": 1,
        "cut": "Ideal",
        "color": "H",
        "clarity": "SI2",
        "x": 6.61,
        "y": 6.65,
        "z": 4.11,
        "depth": 62.0,
        "table": 55.0
    }
```
- json if more instances, for example:
```json
[
    {
        "carat": 1,
        "cut": "Ideal",
        "color": "H",
        "clarity": "SI2",
        "x": 6.61,
        "y": 6.65,
        "z": 4.11,
        "depth": 62.0,
        "table": 55.0
    },
    {
        "carat": 4,
        "cut": "Ideal",
        "color": "H",
        "clarity": "SI2",
        "x": 6.61,
        "y": 6.65,
        "z": 4.11,
        "depth": 62.0,
        "table": 55.0
    }
]
```
Then send the POST request to see the predictions.

#### Challenge 4
For this challenge I will directly provide the answer here. To be fair, I am not expert in this specific area, I have tried to collect some information based on my work experience and online resources. In any case, I tried my best.

Looking for information online, AWS offers many services for different purposes: data storaging (S3), ETL (Glue), training (SageMaker), for exposing API (Lambda) and for monitoring (CloudWatch).

However, I am more familiar with local machine, so the simplest and fastes thing I would do is to get an EC2 and instantiate a docker-compose with all the servicise I need: database (mongo or SQL), jupyter for running pipelines and notebooks, and a Flask application to serve the trained model.
In the current case, GPU for inference is not needed, while with training it could become useful. Consequently, I would get two differents EC2, in order to pay the one with GPU only for the training phase, while I would keep the backend on another one. Then, a shared file system between the two EC2 is used to share models and other files. 
