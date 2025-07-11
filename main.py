import os
import re
from logger import setup_logger
from langchain_core.messages import HumanMessage

from load_cfg import OPENAI_API_KEY, LANGCHAIN_API_KEY, WORKING_DIRECTORY, GOOGLE_API_KEY
from core.workflows import WorkflowManager
from core.language_models import LanguageModelManager

class MultiAgentSystem:
    def __init__(self):
        self.logger = setup_logger()
        self.setup_environment()
        self.lm_manager = LanguageModelManager()
        self.workflow_manager = WorkflowManager(
            language_models=self.lm_manager.get_models(),
            working_directory=WORKING_DIRECTORY
        )

    def setup_environment(self):
        """Initialize environment variables"""
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_TRACING"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "Multi-Agents for DA"


        if not os.path.exists(WORKING_DIRECTORY):
            os.makedirs(WORKING_DIRECTORY)
            self.logger.info(f"Created working directory: {WORKING_DIRECTORY}")

    def parse_input(self, user_input: str):
        """Extracts datapath from user input."""
        match = re.search(r"datapath:(.*)", user_input)
        if match:
            return match.group(1).strip()
        return None

    def run(self, user_input: str) -> None:
        """Run the multi-agent system with user input"""
        datapath = self.parse_input(user_input)
        if not datapath:
            self.logger.error("Could not find 'datapath:' in user input.")
            return

        graph = self.workflow_manager.get_graph()
        
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "sender": "",
            "datapath": datapath,
            "eda_report": "",
            "statistic_report": "",
            "cluster_report": "",
            "visualization_report": "",
            "hypothesis_report": "",
            "reasoning_report": "",
            "total_summary_report": "",
            "final_report": "",

            "transformed_datapath": "",
            "feature_engineering_report": "",
            "model_selection_report": "",
            "model_training_report": "",
            "trained_model_path": "",
            "model_evaluation_report": "",
            "prediction_report": "",
        }

        events = graph.stream(
            initial_state,
            {"recursion_limit": 50},
            stream_mode="values"
        )
        
        for event in events:
            if "messages" in event:
                message = event["messages"][-1]
                if isinstance(message, tuple):
                    print(message, end='', flush=True)
                else:
                    message.pretty_print()

def main():
    """Main entry point"""
    system = MultiAgentSystem()
    
    # user_input = '''
    # datapath:drinks_data.csv
    # Please analyze the 'drinks_data.csv' dataset. Your task is to cluster each instance in the data form into some group, then profile each group based on their digital readiness.
    # '''
    # system.run(user_input)

    user_input_classification = '''
    datapath: edudata_english.csv
    Please analyze the 'edudata_english.csv' dataset and perform a full classification analysis on 'edudata_english.csv' dataset. Now your task is to predict the 'I am willing to share my digital skills with other students' field in the data;
    '''
    system.run(user_input_classification)

if __name__ == "__main__":
    main()