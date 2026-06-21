from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import List , Optional
load_dotenv()

primary_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

class MobileDetails(BaseModel):
    brand: str = Field(description="The brand of the mobile phone (e.g., Apple, Samsung, OnePlus)")
    model_name: str = Field(description="The specific model name and variant details")
    estimated_price_inr: str = Field(description="Approximate market price in INR. Use 'Unknown' if not found.")
    processor: str = Field(description="The processor/chipset details")
    ram_storage_options: List[str] = Field(description="List of available RAM and Storage configurations")
    key_selling_points: List[str] = Field(description="3-4 bullet points highlighting why a customer would buy this phone")

# 3. Bind the Pydantic schema
structured_llm = primary_model.with_structured_output(MobileDetails)

# 4. Create the Prompt Template
retail_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert mobile retail inventory assistant. Extract and provide detailed, accurate technical and market specifications for the requested mobile phone. If a specific detail is completely unknown, output 'N/A'."),
    ("human", "Provide details for the phone: {mobile_query}")
])

# 5. Build the execution chain
extraction_chain = retail_prompt | structured_llm

print("__________ Mobile Inventory Extractor CLI __________")
print("Type 'exit' to end the program\n")

while True:
    mobile_query = input("Enter Mobile Phone Name: ").strip()
    
    if mobile_query.lower() == "exit":
        print("Exiting program.")
        break
        
    if not mobile_query:
        print("Please enter a valid phone name.\n")
        continue
        
    print("\nFetching and structuring data from LLaMA 3.3...")
    try:
        # Execute the chain
        result = extraction_chain.invoke({"mobile_query": mobile_query})
        
        # Automatically print the entire Pydantic object as beautifully formatted JSON
        print("\n" + "="*40)
        print("DATABASE READY JSON:")
        print(result.model_dump_json(indent=4))
        print("="*40 + "\n")
        
    except Exception as e:
        print(f"\n[SYSTEM ERROR]: An error occurred during extraction: {e}\n")
