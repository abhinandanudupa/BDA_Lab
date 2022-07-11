import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class OddEvenMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

	public void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, IntWritable>.Context context)
			throws IOException, InterruptedException {
		
		String numStr = value.toString();
		Integer number = Integer.parseInt(numStr);
		
		String oddOrEven = "";
		if (number % 2 == 0) {
			oddOrEven = "even"; 
		}
		else {
			oddOrEven = "odd";
		}
		context.write(new Text(oddOrEven), new IntWritable(1));

	}
}
