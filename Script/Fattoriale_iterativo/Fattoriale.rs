use std::env;

fn fattoriale_iter(n: u128) -> u128 {
    let mut risultato: u128 = 1;
    for i in 1..=n {
        risultato *= i;
    }
    risultato
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Uso: {} <numero>", args[0]);
        std::process::exit(1);
    }

    let n: u128 = args[1].parse().expect("Inserisci un numero valido");
    let risultato = fattoriale_iter(n);
    println!("Fattoriale iterativo({}) = {}", n, risultato);
}
