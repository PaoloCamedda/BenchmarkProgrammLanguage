public class Fibonacci {
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n-1) + fibonacci(n-2);
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java FibonacciRec <numero>");
            return;
        }
        int n = Integer.parseInt(args[0]);
        System.out.println("Fibonacci(" + n + ") = " + fibonacci(n));
    }
}
