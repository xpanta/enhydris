import py4j.GatewayServer;
import java.util.Hashtable;
/**
* <h1>Class for connecting JAVA from Python</h1>
* This class is an entry point to connect JAVA from python to utilise the functionality of
* weka data mining and machine learning library. Weka is used due to its rich and stable features.
* This class provide access to our implementation of time series forecasting that is implemented 
* using weka time series forecasting plugin
*
* @author  Adeel Hashmi
* @version 1.0
* @since   30-03-2014
*/
public class TimeSeriesEntry {

    private static GatewayServer gatewayServer;
    private TimeSeries ts;
    private Hashtable<String,TimeSeries> ht;
    
    /**
     * This method instanties TimeSeries. TimeSeries is an implementation of time series forecasting  
     * @see         TimeSeries
     */     
    public TimeSeriesEntry() {
    		ht = new Hashtable<String,TimeSeries>();
    }
    
    /**
     * This method returns TimeSeries object.  
     * @return      TimeSeries object
     * @see         TimeSeries
     */         
    public TimeSeries getTimeSeries(String userid) {
    	if(ht.containsKey(userid))
    	{
    		ts = ht.get(userid);
    	}
    	else
    	{
    		ts = new TimeSeries();
    	}
    	return ts;
    }
    

    /**
     * This method shuts the py4j gateway server  
     * @see         py4j.GatewayServer
     */             
    public void shutGateway() {
    	gatewayServer.shutdown();
    }
    
    /**
     * This is the main entry point method for communication between JAVA and python
     * In production environment this gateway server needs to be started on system startup
     * In case of JVM crash, this also needs to be restarted. It is possible that abrupt crash
     * might leave the main port open so the old port needed to be closed or any other freeport can be
     * chosen for gateway server. Whatever the port is selected, that port number has to be 
     * available in python too so python can connect to this Gateway server  
     * @see         py4j.GatewayServer
     */      
    public static void main(String[] args) {
    	// default local host port use by gateway server (25333)
    	//gatewayServer = new GatewayServer(new TimeSeriesEntry(),25336);
    	try{
    		gatewayServer = new GatewayServer(new TimeSeriesEntry()); //instantiates the gatewayserver for communicating with python on default port
    		gatewayServer.start();	//start the server
    		System.out.println("Gateway Server Started");
    	}catch(Exception exp){System.out.println("Gateway Server not Started, please make sure default port (25333) is free");}
    }	
}//--end class

