import java.io.BufferedReader;
import java.io.FileReader;
import java.util.List;
import weka.core.Instances;
import weka.classifiers.AbstractClassifier;
import weka.classifiers.functions.LinearRegression;
import weka.classifiers.functions.GaussianProcesses;
import weka.classifiers.functions.MultilayerPerceptron;
import weka.classifiers.evaluation.NumericPrediction;
import weka.classifiers.timeseries.WekaForecaster;

/**
* <h1>Forecasting using statistical technique and Neural networks</h1>
* This class converts the json input of time series and convert it into arff file format
* This arff file is then use to for time series forecasting using statistical technique
* and neural network algorithm (MLP). The output of forecasting is return as comman seprated 
* list of values.
*
* @author  Adeel Hashmi
* @version 1.0
* @since   2014-03-31
*/
public class TimeSeries {

	private Thread t1,t2,t3;
	private Arff arffyear,arffday,arffelec;
	
	public TimeSeries()
	{
		arffyear = new Arff();
		arffday  = new Arff();
		arffelec = new Arff();
		t1 	     = new Thread(arffyear);
		t2 	     = new Thread(arffday);
		t3 	     = new Thread(arffelec);
		t1.start();
		t2.start();
		t3.start();
	}
	
	public boolean getArffelectricstatus()
	{
		return arffelec.getArffstatus();
	}
	
	public String getelectricArff()
	{
		return arffelec.getArff();
	}	
	
	public boolean getArffyearstatus()
	{
		return arffyear.getArffstatus();
	}	
	
	public String getyearlyArff()
	{
		return arffyear.getArff();
	}	
	
	public boolean getArffdaystatus()
	{
		return arffday.getArffstatus();
	}	
	
	public String getdayArff()
	{
		return arffday.getArff();
	}	
	
	public void safeThread()
	{
		if(arffyear!=null)
		{
			arffyear.terminate();
		}
		
		if(arffday!=null)
		{
			arffday.terminate();
		}
		
		if(arffelec!=null)
		{
			arffelec.terminate();
		}
		//System.out.println("All threads terminated..");
	}//--end function
		
	public void writeyearlyArff(String data,String floc)
	{
		arffyear.threadEntry(data,floc);
	}

	public void writedayArff(String data,String floc)
	{
		arffday.threadEntry(data,floc);
	}

	public void writelectricArff(String data,String floc)
	{
		arffelec.threadEntry(data,floc);
	}
	
    /**
     * This method simply returns the GaussianProcesses object
     * this will be used for forecasting  
     * @return      algorithm to be used for forecasting
     * @see         weka.classifiers.AbstractClassifier, weka.classifiers.functions.GaussianProcesses
     */       
    public GaussianProcesses getGaussian()
    {
    	return new GaussianProcesses();	
    }

    /**
     * This method simply returns the LinearRegression object
     * this will be used for forecasting  
     * @return      algorithm to be used for forecasting
     * @see         weka.classifiers.AbstractClassifier, weka.classifiers.functions.LinearRegression
     */           
    public LinearRegression getLinear()
    {
    	return new LinearRegression();
    }

    /**
     * This method simply returns the MultilayerPerceptron object
     * this will be used for forecasting  
     * @return      algorithm to be used for forecasting
     * @see         weka.classifiers.AbstractClassifier, weka.classifiers.functions.MultilayerPerceptron
     */               
    public MultilayerPerceptron getMLP()
    {
    	return new MultilayerPerceptron();
    }

    /**
     * This method forecast the timeseries. The timeseries implemetation is based on weka forecasting plugin  
     *
     * @param  ftemp arff absolute file location to be used for forecasting 
     * @param  units this is number of steps/units/months/years etc.. in the future to predict the forecasting 
     * @param  algrithm one of the forecasting algorithms for forecasting 
     * @param  col  this is the column name of the arff file to be used for forecasting 
     * @return results return common seperated values of forecasting, if any exception occured then it returns null
     * @see         weka.classifiers.timeseries.WekaForecaster, weka.classifiers.AbstractClassifier, weka.classifiers.functions
     */        
	public String getForecast(String ftemp,int units,AbstractClassifier algorithm,String fcol)
	{
		String results = "";
        try {
            // path to the Timeseries data for forecasting
            String pathToData = ftemp;
            
            // load the timeseries data
            Instances ts = new Instances(new BufferedReader(new FileReader(pathToData)));

            // new forecaster
            WekaForecaster forecaster = new WekaForecaster();

            // set the targets we want to forecast. This method calls
            // setFieldsToLag() on the lag maker object for us
            forecaster.setFieldsToForecast(fcol);

            // default underlying classifier is SMOreg (SVM) - we'll use
            // gaussian processes for regression instead
            forecaster.setBaseForecaster(algorithm);

            forecaster.getTSLagMaker().setTimeStampField("Date"); // date time stamp
            //forecaster.getTSLagMaker().setMinLag(1);
            //forecaster.getTSLagMaker().setMaxLag(12); // monthly data

            // add a month of the year indicator field
            //forecaster.getTSLagMaker().setAddMonthOfYear(true);

            // add a quarter of the year indicator field
            //forecaster.getTSLagMaker().setAddQuarterOfYear(true);

            // build the model
            forecaster.buildForecaster(ts, System.out);

            // prime the forecaster with enough recent historical data
            // to cover up to the maximum lag. In our case, we could just supply
            // the 12 most recent historical instances, as this covers our maximum
            // lag period
            forecaster.primeForecaster(ts);
            
            // forecast for 12 units (months) beyond the end of the
            // training data
            List<List<NumericPrediction>> forecast = forecaster.forecast(units, System.out);
            	
            // output the predictions. Outer list is over the steps; inner list is over
            // the targets
            for (int i = 0; i < units; i++) {
                List<NumericPrediction> predsAtStep = forecast.get(i);
                for (int j = 0; j < 1; j++) {
                    NumericPrediction predForTarget = predsAtStep.get(j);
                    results = results+predForTarget.predicted()+",";
                }
            }
			
            //setEnd(ftemp); //delete the temporary arff file
            // we can continue to use the trained forecaster for further forecasting
            // by priming with the most recent historical data (as it becomes available).
            // At some stage it becomes prudent to re-build the model using current
            // historical data.

        } catch (Exception ex) {
        	return null;
        }		
        return results;
	}//--end function
}
