function fattorialeIter(n) {
  let risultato = 1;
  for (let i = 1; i <= n; i++) {
    risultato *= i;
  }
  return risultato;
}

if (process.argv.length !== 3) {
  console.log(`Uso: node ${process.argv[1]} <numero>`);
  process.exit(1);
}

const n = parseInt(process.argv[2], 10);
console.log(`Fattoriale iterativo(${n}) = ${fattorialeIter(n)}`);
