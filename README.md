# Doris

This repo shows the constructions of OXT [1], HXT[2], ConjFilter[3] and Doris[4].

## Environment Configuration

- ubuntu20.04
- python3.8
- [pypbc](https://github.com/debatem1/pypbc)
    ```sh
    # install requirements libraries
    sudo apt update 
    sudo apt-get install flex bison libgmp-dev make

    # Download PBC source code and compile it
    cd ~ &&
    wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz &&
    tar -xf pbc-0.5.14.tar.gz &&
    cd pbc-0.5.14 &&
    ./configure --prefix=/usr --enable-shared &&
    make &&
    sudo make install &&
    cd .. 

    # re-configure the ldconfig
    sudo ldconfig

    # Install the pypbc
    git clone https://github.com/debatem1/pypbc &&
    cd pypbc &&
    sudo pip3 install .
    cd ..
    ```
- install source code and additional python libraries
    ```sh
    git clone https://github.com/CDSecLab/Doris.git
    cd Doris
    pip3 install -r requirements.txt 
    ```


## File Structure

```
.
├── README.md
├── requirements.txt
|
| // the constructions of OXT, HXT, ConjFilter and Doris
├── ConjFilter_alter.py // ConjFilter that support single keyword search
├── ConjFilter_ori.py // ConjFilter original scheme
├── Doris_XF.py
├── HXT.py
├── OXT.py
|
├── data // database of enron and enwiki, including indexes and inverted indexes
│   ├── enron_index0.csv // 10^2 key/value pairs
│   ├── enron_index1.csv // 10^3 key/value pairs
│   ├── enron_index2.csv // 10^4 key/value pairs
│   ├── enron_index3.csv // 10^5 key/value pairs
│   ├── enron_index4.csv // 10^6 key/value pairs
│   ├── enron_inverted0.csv
│   ├── enron_inverted1.csv
│   ├── enron_inverted2.csv
│   ├── enron_inverted3.csv
│   ├── enron_inverted4.csv
|   ├── ...
|
├── Utils 
│   ├── BF.py 
│   ├── SHVE.py 
│   ├── SSPE_XF.py
│   ├── TSet.py
│   ├── XorFilter.py
│   ├── cfg.py
│   ├── cryptoUtils.py
│   ├── fileUtils.py
│   ├── pbcUtils.py
│   └── test // examples and tests of tools
|
| // experiment
├── multi_keywords_exp.py
├── setup_exp.py
├── tools_exp.py
└── two_keywords_exp.py
```

## Examples

Running the full experiment requires at least 128GB of memory, which is lightweight here, so you need to make sure you have at least 8GB of memory when running the experiment below.

### protocol

```sh
python3 OXT.py
python3 HXT.py
python3 ConjFilter_alter.py
python3 Doris_XF.py
```

- Test whether the environment is configured successfully and run four protocols

### tools experiment

```sh
python3 tools_exp.py
```

- This demo compares the storage and query overhead of the two tools
    - SHVE in HXT[2]: `Utils/SHVE.py`
    - SSPE in Doris[4]: `Utils/SSPE_XF.py`
- Log output to `log/tools_enc_exp.log`,`log/tools_query_exp.log` 
- use about 5 min, 8 GB RAM
- If `FileNotFoundError` appears, create a folder `log` in the project root directory


### setup experiment

```sh
python3 setup_exp.py
```

- This demo compares the storage overhead and computing overhead consumed by the four schemes when creating EDBs
- running on both large and small databases
    - enron database
    - enwiki database
- Log output to `log/setup_enron_exp.log`,`log/setup_enwiki_exp.log` 
- use about 30 min, 8 GB RAM


### two-keyword experiment

```sh
python3 two_keywords_exp.py
```

- The demo compares the computing overhead and communication overhead of the four schemes in the query of two keywords
- Since the query time in this experiment is only related to the number of documents corresponding to $w_1$, a small database can be simulated for the experiment to prevent memory overflow
- Log output to `log/two_keywords_exp.log`
- use about 20 min

### multi-keyword experiment

```sh
python3 multi_keywords_exp.py
```

- Fixed w1, changed the number of query keywords, and compared the computing overhead and communication overhead of the four schemes
- Same as the two-keyword experiment, we used a small dataset to simulate the original dataset
- Log output to `log/multi_keywords_exp.log`
- use about 50 min

## Contact Us

- ylwang@xupt.edu.cn
- jfwang@xidian.edu.cn


## Reference

[1]. David Cash, Stanislaw Jarecki, Charanjit S. Jutla, Hugo Krawczyk, Marcel-Catalin Rosu, Michael Steiner: Highly-Scalable Searchable Symmetric Encryption with Support for Boolean Queries. CRYPTO 2013: 353-373.

[2]. Shangqi Lai, Sikhar Patranabis, Amin Sakzad, Joseph K. Liu, Debdeep Mukhopadhyay, Ron Steinfeld, Shifeng Sun, Dongxi Liu, Cong Zuo: Result Pattern Hiding Searchable Encryption for Conjunctive Queries. CCS 2018: 745-762.

[3]. Sarvar Patel, Giuseppe Persiano, Joon Young Seo, Kevin Yeo: Efficient Boolean Search over Encrypted Data with Reduced Leakage. ASIACRYPT 2021: 577-607.

[4]. Yunling Wang, Shi-Feng Sun, Jianfeng Wang, Xiaofeng Chen, Joseph K.Liu, and Dawu Gu. Practical Non-interactive Encrypted Conjunctive Search with Leakage Suppression. CCS 2024.

