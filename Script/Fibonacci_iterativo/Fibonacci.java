public class Fibonacci{
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        int a = 0, b = 1, c = 0;
        for (int i = 2; i <= n; i++) {
            c = a + b;
            a = b;
            b = c;
        }
        return b;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java Fibonacci <numero>");
            return;
        }
        int n = Integer.parseInt(args[0]);
        System.out.println("Fibonacci(" + n + ") = " + fibonacci(n));
    }
}
