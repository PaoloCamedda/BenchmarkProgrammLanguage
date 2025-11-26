function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

const args = process.argv.slice(2);
if (args.length !== 1) {
    console.log(`Uso: node fibonacci_rec.js <numero>`);
    process.exit(1);
}

const n = parseInt(args[0], 10);
console.log(`Fibonacci(${n}) = ${fibonacci(n)}`);
