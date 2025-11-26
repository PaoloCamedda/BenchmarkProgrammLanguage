use std::env;

fn fattoriale_rec(n: u128) -> u128 {
    if n == 0 || n == 1 {
        1
    } else {
        n * fattoriale_rec(n - 1)
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Uso: {} <numero>", args[0]);
        std::process::exit(1);
    }

    let n: u128 = args[1].parse().expect("Inserisci un numero valido");

    if n > 34 {
        eprintln!("Attenzione: {}! non può essere calcolato con i tipi nativi (overflow oltre 34!)", n);
        std::process::exit(1);
    }

    let risultato = fattoriale_rec(n);
    println!("Fattoriale ricorsivo({}) = {}", n, risultato);
}
