import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws Exception {
        // 打印命令行参数，每个参数占一行
        System.out.println("Received command line arguments:");
        for (String arg : args) {
            System.out.println(arg);
        }

        // 创建一个大约100MB的数组
        int size = 25 * 1024 * 1024; // 大约100MB (每个int是4字节)
        int[] bigArray = new int[size];
        Arrays.fill(bigArray, 1); // 填充数组以确保内存被分配

        // 读取并打印输入数据
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter input (type 'end' to finish):");
        String inputLine;
        while ((inputLine = reader.readLine()) != null && !inputLine.equals("end")) {
            System.out.println("Received input: " + inputLine);
        }

        // 运行约10秒
        System.out.println("Running for about 10 seconds...");
        Thread.sleep(10000);

        System.out.println("Finished running.");
    }
}
