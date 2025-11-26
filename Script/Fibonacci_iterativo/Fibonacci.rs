use std::env;

fn fibonacci(n: u32) -> u64 {
    if n <= 1 {
        return n as u64;
    }
    let mut a: u64 = 0;
    let mut b: u64 = 1;
    for _ in 2..=n {
        let c = a + b;
        a = b;
        b = c;
    }
    b
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Uso: {} <numero>", args[0]);
        return;
    }
    let n: u32 = args[1].parse().expect("Inserisci un numero valido");
    println!("Fibonacci({}) = {}", n, fibonacci(n));
}
