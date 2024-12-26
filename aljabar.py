import numpy as np

# Fungsi untuk menanyakan apakah masalah maximasi atau minimasi
def input_jenis_optimasi():
    while True:
        pilihan = input("Jenis optimasi (max/min): ").lower()
        if pilihan.startswith('max') or pilihan.startswith('min'):
            return pilihan.startswith('max')
        print("Error: Pilih 'max' atau 'min'!")

# Fungsi untuk input koefisien fungsi tujuan (Z = ax + by)
def input_fungsi_tujuan():
    print("\nFungsi Tujuan Z = ax + by")
    print("Contoh input untuk Z = 3x + 4y → ketik: 3 4")
    while True:
        try:
            koef = list(map(float, input("Masukkan a b: ").split()))
            if len(koef) == 2:
                return koef
            print("Error: Masukkan 2 nilai!")
        except ValueError:
            print("Error: Masukkan angka yang valid!")

# Fungsi untuk input kendala-kendala
def input_kendala():
    while True:
        try:
            n = int(input("\nJumlah kendala: "))
            if n > 0:
                break
            print("Error: Minimal 1 kendala!")
        except ValueError:
            print("Error: Masukkan angka!")
    
    print("\nFormat kendala: a b tanda c")
    print("Tanda: 1(≤) 2(≥) 3(=)")
    print("Contoh: 2x + 3y ≤ 12 → ketik: 2 3 1 12")
    
    kendala = []      
    tanda = []        
    nilai_kanan = []  
    
    # Input setiap kendala
    for i in range(n):
        while True:
            try:
                inp = input(f"Kendala {i+1}: ").split()
                if len(inp) != 4:
                    print("Error: Masukkan 4 nilai!")
                    continue
                
                koef = list(map(float, inp[:-2]))
                t = int(inp[-2])
                if t not in [1, 2, 3]:
                    print("Error: Tanda harus 1, 2, atau 3!")
                    continue
                
                nilai = float(inp[-1])
                
                kendala.append(koef)
                tanda.append(t)
                nilai_kanan.append(nilai)
                break
            except ValueError:
                print("Error: Masukkan angka yang valid!")
    
    return kendala, tanda, nilai_kanan

# Fungsi untuk mencari titik-titik potong antar garis kendala
def titik_potong(kendala, nilai_kanan):
    n = len(kendala)
    titik = [(0, 0)]  
    
    for i in range(n):
        # Cari titik potong dengan sumbu Y
        if kendala[i][1] != 0:
            y_val = nilai_kanan[i] / kendala[i][1]
            if y_val >= 0:
                titik.append((0, y_val))
        
        # Cari titik potong dengan sumbu X
        if kendala[i][0] != 0:
            x_val = nilai_kanan[i] / kendala[i][0]
            if x_val >= 0:
                titik.append((x_val, 0))
    
        # Cari titik potong antar garis kendala
        for j in range(i+1, n):
            try:
                A = np.array([[kendala[i][0], kendala[i][1]], 
                            [kendala[j][0], kendala[j][1]]])
                b = np.array([nilai_kanan[i], nilai_kanan[j]])
                
                solusi = np.linalg.solve(A, b)
                if all(s >= 0 for s in solusi):
                    titik.append(tuple(solusi))
            except:
                continue
    
    # Bulatkan nilai dan hapus titik yang duplikat
    return list(set([(round(x, 4), round(y, 4)) for x, y in titik]))

# Fungsi untuk mengecek apakah suatu titik memenuhi semua kendala
def cek_kendala(titik, kendala, tanda, nilai_kanan):
    for i in range(len(kendala)):
        nilai = kendala[i][0] * titik[0] + kendala[i][1] * titik[1]
        if tanda[i] == 1 and nilai > nilai_kanan[i] + 1e-10:      
            return False
        elif tanda[i] == 2 and nilai < nilai_kanan[i] - 1e-10:    
            return False
        elif tanda[i] == 3 and abs(nilai - nilai_kanan[i]) > 1e-10:  
            return False
    return True

# Program utama
def main():
    print("PROGRAM LINEAR PROGRAMMING METODE ALJABAR")
    print("=========================================")
    
    # Tentukan jenis optimasi (max/min)
    is_max = input_jenis_optimasi()
    
    # Input fungsi tujuan
    koef_tujuan = input_fungsi_tujuan()
    
    # Input semua kendala
    kendala, tanda, nilai_kanan = input_kendala()
    
    # Cari semua titik potong yang mungkin
    titik_feasible = titik_potong(kendala, nilai_kanan)
    
    # Evaluasi setiap titik potong
    hasil_valid = []
    for titik in titik_feasible:
        if cek_kendala(titik, kendala, tanda, nilai_kanan):
            z = koef_tujuan[0] * titik[0] + koef_tujuan[1] * titik[1]
            hasil_valid.append((titik, z))
    
    # Tampilkan hasil perhitungan
    print("\nHASIL PERHITUNGAN:")
    print("-----------------")
    
    if not hasil_valid:
        print("Tidak ada solusi yang memenuhi kendala!")
        return
    
    print("\nTitik yang memenuhi:")
    for titik, nilai in hasil_valid:
        print(f"({titik[0]}, {titik[1]}) → Z = {int(nilai)}")  
    
    # Tentukan solusi optimal (max/min) sesuai pilihan di awal
    optimal = max(hasil_valid, key=lambda x: x[1]) if is_max else min(hasil_valid, key=lambda x: x[1])
    
    print("\nSOLUSI OPTIMAL:")
    print(f"Titik: ({optimal[0][0]}, {optimal[0][1]})")
    print(f"Z = {int(optimal[1])}") 

if __name__ == "__main__":
    main()