import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class OddEvenReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	public void reduce(Text key, Iterable<IntWritable> values, 	Reducer<Text, IntWritable, Text, IntWritable>.Context context)
	throws IOException, InterruptedException {
		int count = 0;
		for (IntWritable value : values) {
			System.out.println(value.get());
			count++;
		}
		context.write(key, new IntWritable(count));
	}
}