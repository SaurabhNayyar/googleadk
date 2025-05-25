from google.adk.tools import BaseTool, ToolContext
from typing import Dict, Any, Optional

def validateFlightRequestDetails_beforeToolCallback(tool:BaseTool, args:Dict[str, Any], tool_context:ToolContext)->Optional[dict]:
    """
    Validates that all required fields are present in the provided data.
    Args:
        tool(BaseTool): This provides access to tool name, description etc.
        args(Dict): Dictionary of all arguments to the tool.
        tool_context: This provides the context of the tool.
    Returns:
        Optionally, returns a dictionary.
    """
    missing_fields=[]
    agent_name = tool_context.agent_name
    tool_name = tool.name
    
    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")

    if tool_name == 'search_flights' and args.get('flight_date','')=='':
        missing_fields.append('flight_date')
    if tool_name == 'search_flights' and args.get('from_city','')=='':
        missing_fields.append('from_city')
    if tool_name == 'search_flights' and args.get('to_city','')=='':
        missing_fields.append('to_city')
    if tool_name == 'search_flights' and args.get('adults_count', None)==None:
        missing_fields.append('adults_count')
    if tool_name == 'search_flights' and args.get('children_count', None)==None:
        missing_fields.append('children_count')
    if tool_name == 'search_flights' and args.get('infants_in_seat', None)==None:
        missing_fields.append('infants_in_seat')
    if tool_name == 'search_flights' and args.get('infants_on_lap',None)==None:
        missing_fields.append('infants_on_lap')
    if tool_name == 'search_flights' and args.get('trip_detail','')=='':
        missing_fields.append('trip_detail')
    if tool_name == 'search_flights' and args.get('seat_class','')=='':
        missing_fields.append('seat_class')
        
        
    # Convert List to Dictionary
    # missing_fields_dict = {str(index): item for index, item in enumerate(missing_fields)}
    
    print(f"-- MISSING FIELDS --\n")
    
    if(len(missing_fields)>0):
        print({"status":"error",
                "message":f"missing_fields: {','.join(missing_fields)}"})
        return {"status":"error",
                "message":f"missing_fields: {','.join(missing_fields)}"}
    else:
        return None
        
