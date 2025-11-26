function fibonacci(n) {
    if (n <= 1) return n;
    let a = 0, b = 1, c;
    for (let i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

const args = process.argv.slice(2);
if (args.length !== 1) {
    console.log(`Uso: node fibonacci_js.js <numero>`);
    process.exit(1);
}

const n = parseInt(args[0], 10);
console.log(`Fibonacci(${n}) = ${fibonacci(n)}`);
