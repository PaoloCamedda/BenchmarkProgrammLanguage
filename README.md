# BenchmarkProgrammLanguage

Programmazione egreen e test sul consumo energetico dei vari linguaggi di programmazione 



## Indice 
* [Installazione](#installazione)
* [Utilizzo](#utilizzo)
* [Licenza](#licenza)




## Installazione
i test sono stati basati su ambiente linux i3 con cpu intel cosi da avere a disposizione i contatori RAPL
I test sono stati efettuati su Ubuntu 24.04.3 LTS
e processore intel core7 

Per configurare il progetto in locale, segui questi passaggi:

### Prerequisiti
* Python 3.12.3
* Node.js v18.19.1
* gcc 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04) 
* openjdk version "21.0.9" 2025-10-21
* rustc 1.91.1 (ed61e7d7e 2025-11-07)
* hyperfine 




### Passaggi
1. Installre ambiente grafico i3 linux 
   ```bash
   sudo apt install i3
   ```

2. Entrare nel ambiente i3 e rimuovere il blocco dello schermo e lo standby 
    ```bash
   xset s off
   xset dpms 0 0 0
   ```

3. rimuovere le conessioni (Facoltativo, on se si vuole riattivare ) 
   ```bash
   nmcli radio all off
   ```

4. Clona il repository:
   ```bash
   git clone [https://github.com/tuo-utente/tuo-progetto.git](https://github.com/PaoloCamedda/BenchmarkProgrammLanguage.git)
   cd BenchmarkProgrammLanguage
   chmod +x run_benchmark.sh
   ```


## Utilizzo 
1. lanciare il comado per ottenere le informazioni 
      ```bash
   ./run_benchmark.sh -h 
   ```
esempio
      ```bash
   ./run_benchmark.sh -r 5 -w 0 -n 5-20:5 -a fib -t rc -l py
   ```

2. se si è lanciato il comando con range di numeri non usare -a ms,qs e usare il parser per range troverete i risultati nella cartella Results/csv altrimenti parser_single.py
   ```bash
   sudo chown -R $USER:$USER Results
   python3 parser_range.py
   ```
   

3. per visualizzare i grafici eseguire i plot a seconda di cio che si vuole ottenrere 
   ```bash
   python3 plot_range.py
   ```
![Comparazione](.comparazione.png)