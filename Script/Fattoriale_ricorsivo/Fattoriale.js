function fattorialeRec(n) {
  if (n === 0 || n === 1) {
    return 1;
  }
  return n * fattorialeRec(n - 1);
}

if (process.argv.length !== 3) {
  console.log(`Uso: node ${process.argv[1]} <numero>`);
  process.exit(1);
}

const n = parseInt(process.argv[2], 10);
console.log(`Fattoriale ricorsivo(${n}) = ${fattorialeRec(n)}`);
