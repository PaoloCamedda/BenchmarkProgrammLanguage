public class Fattoriale {

    public static long fattoriale(int n) {
        long risultato = 1;
        for (int i = 1; i <= n; i++) {
            risultato *= i;
        }
        return risultato;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java Fattoriale <numero>");
            return;
        }

        int n = Integer.parseInt(args[0]);
        System.out.println("Fattoriale iterativo(" + n + ") = " + fattoriale(n));
    }
}
