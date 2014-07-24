import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Iterator;
import java.util.UUID;

import org.json.JSONArray;
import org.json.JSONObject;

public class Arff implements Runnable {

	private String data = "";
	private String floc = "";
	private final int DURATION=1000; // in milliseconds
	private volatile boolean go = false;
	private volatile boolean running = true;
	
    /**
     * This method takes the file location and delete that file from a directory  
     * @param  floc ab absolute file location to be deleted from directory
     * @return      return boolean value indicating deletion status: true on success otherwise false
     * @see         File
     */    
    public boolean deleteArff(String floc)
    {
    	try{
    		File ftemp = new File(floc);
    		ftemp.delete();
    	}catch(Exception io){return false;}
    	return true;
    }
    
	public String getArff()
	{
		String fname = UUID.randomUUID().toString(); //generates unique filename
		String floc="";
		try{
			File ftemp = File.createTempFile(fname,".arff");
			floc = ftemp.getAbsolutePath();
		}catch(Exception exp){return null;}
		return floc;
	}

	public boolean getArffstatus()
	{
		return go;
	}

    public void threadEntry(String data,String floc)
    {
    	this.data = data;
    	this.floc = floc;
    	go = true;
    }
    
    public void terminate() 
    {
        running = false;
    }   
    
	public void run()
	{
		System.out.println("starting thread..");
		while(running)
		{
			if(go)
				setTimeSeriesdata(this.data,this.floc);
		
			try{
				Thread.sleep(DURATION);
			}catch(Exception e){}
				
		}
	}//--end run
	
    /**
     * This method takes the timeseries json object and convert it into 
     * arff format. weka timeseries forecast only takes arff file format
     * as input and use then does processing, there is no way to to process
     * in memory arff for providing input to input. See arff file format for
     * more details
     *
     * @param  json json file consists of data to process in this format: ("date", "value") 
     * @return      absolute location of the arff file created
     * @see         File, FileWriterm BufferedWriter, org.json.JSONObject, org.json.JSONArray
     */      
    public void setTimeSeriesdata(String json,String floc)
    {
    	//String fname = UUID.randomUUID().toString(); //generates unique filename
    	//String floc  = "";
    	//following declaration for arff file format
    	String Rel   = "@RELATION";
    	String Attr  = "@ATTRIBUTE";
    	String Num   = "NUMERIC";
    	String Date  = "Date";
    	String fmt   = "yyyy-MM-dd";
    	String line = "@DATA\n";
    	//end of arff declarations
    	
    	try{
    		JSONObject jsonobj; //see org.json documentation for details
        	//File ftemp = File.createTempFile(fname,".arff"); //create temp file in /temp folder, make sure it is writable
    		File ftemp = new File(floc);
    		String fname = ftemp.getName();
        	//floc = ftemp.getAbsolutePath();	//absolute file path
			FileWriter fw = new FileWriter(ftemp.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);    		
			
			JSONArray jsonarr = new JSONArray(json); //see org.json documentation for details
			
			//following piece of code block if change or if order of file writing is changed then arff file format might get corrupted. before any change please make sure
			//to understand the arff file format
    		bw.write(Rel+" "+fname+"\n"); //see arff file format
    		
    		for(int i=0;i<jsonarr.length();i++)
    		{
    			jsonobj = jsonarr.getJSONObject(i);
    			Iterator iter = jsonobj.keys();
    			while(iter.hasNext())
    			{
    				String key1 = iter.next().toString(); //first key from json, data
    				String key2 = iter.next().toString(); //second key from json, unit or cost or other.., depends on what is provided
	    			Object d = jsonobj.get(key1); //get value (date)
	    			Object u = jsonobj.get(key2); //get second value
	    			try{Double.valueOf(u.toString());} //if value is not a valid number (integer, long or float or double or empty value or nan etc.. or there is a gap in data)
	    			catch(NumberFormatException e){u=0.0;} //make it zero
	    			line = line + (d+","+u+"\n"); 
	    			if(i==0)
	    			{
	    				bw.write(Attr+" "+Date+" "+key1+" '"+fmt+"'\n"); 
	    				bw.write(Attr+" "+key2+" "+Num+"\n");
	    			}
	    				
    			}
    		}
    		bw.write(line);
    		//end of code block
			bw.close();
			go = false;
    	}
    	catch(Exception e){go=false;} 
    }//--end

}

