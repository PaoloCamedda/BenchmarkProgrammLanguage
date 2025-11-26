public class Fattoriale {

    public static long fattoriale(int n) {
        if (n == 0 || n == 1) {
            return 1;
        }
        return n * fattoriale(n - 1); // chiamata ricorsiva corretta
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java Fattoriale <numero>");
            return;
        }

        int n = Integer.parseInt(args[0]);
        System.out.println("Fattoriale ricorsivo(" + n + ") = " + fattoriale(n));
    }
}
