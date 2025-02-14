from fastapi import FastAPI
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd
from src.model import recommend, output_recommended_recipes
import os

dataset = None  # Initialize as None


app = FastAPI()


class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input:conlist(float, min_items=9, max_items=9)
    ingredients:list[str]=[]
    params:Optional[params]


class Recipe(BaseModel):
    Name:str
    CookTime:str
    PrepTime:str
    TotalTime:str
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None



@app.on_event("startup")
async def load_dataset():
    global dataset
    dataset_path = os.path.join(os.getcwd(), "Data/dataset.csv")
    if os.path.exists(dataset_path):
        dataset = pd.read_csv(dataset_path, compression='gzip')
    else:
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}