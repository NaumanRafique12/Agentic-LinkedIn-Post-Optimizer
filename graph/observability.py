
from langsmith import traceable,Client

@traceable(name='agent_run_summary')
def log_run_summary(metrics : dict):
  return metrics

@traceable(name='agentic-linkedin-post-run')
def run_workflow(workflow,state,config):
  final_state =  workflow.invoke(state,config=config)
  client = Client()
  runs = list(client.list_runs(
    project_name="agentic-linkedin-post-optimizer",
    run_name="agentic-linkedin-post-run",
    limit=1,
    ))

  if runs:
        run = runs[0]
        actual_costs = {
            "prompt_tokens": getattr(run, 'prompt_tokens', 0),
            "completion_tokens": getattr(run, 'completion_tokens', 0),
            "total_tokens": getattr(run, 'total_tokens', 0),
            "total_cost_usd": getattr(run, 'total_cost', 0.0)
        }
        
        for key, val in actual_costs.items():
            final_state['run_metrics'][key] = val
    
  return final_state
