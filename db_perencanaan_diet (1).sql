-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Feb 2026 pada 16.12
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_perencanaan_diet`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_catatan_air`
--

CREATE TABLE `tbl_catatan_air` (
  `id_catatan` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `jumlah_ml` int(11) NOT NULL,
  `waktu_minum` time DEFAULT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_catatan_air`
--

INSERT INTO `tbl_catatan_air` (`id_catatan`, `user_id`, `jumlah_ml`, `waktu_minum`, `tanggal`) VALUES
(1, 2, 1000, '22:02:09', '2026-02-10'),
(2, 2, 1000, '22:02:10', '2026-02-10'),
(3, 2, 1000, '22:02:10', '2026-02-10'),
(4, 2, 1000, '22:02:10', '2026-02-10'),
(5, 2, 1000, '22:02:10', '2026-02-10');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_catatan_berat`
--

CREATE TABLE `tbl_catatan_berat` (
  `id_catatan` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `berat_kg` decimal(5,2) NOT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_catatan_makan`
--

CREATE TABLE `tbl_catatan_makan` (
  `id_catatan` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `id_makanan` int(11) NOT NULL,
  `waktu_makan` enum('sarapan','siang','malam','camilan') NOT NULL,
  `jumlah_porsi` decimal(5,2) NOT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_catatan_makan`
--

INSERT INTO `tbl_catatan_makan` (`id_catatan`, `user_id`, `id_makanan`, `waktu_makan`, `jumlah_porsi`, `tanggal`) VALUES
(1, 2, 2, '', 1.00, '2026-02-10'),
(2, 2, 17, '', 1.00, '2026-02-10');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_catatan_olahraga`
--

CREATE TABLE `tbl_catatan_olahraga` (
  `id_catatan` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `id_olahraga` int(11) NOT NULL,
  `durasi_menit` int(11) NOT NULL,
  `kalori_terbakar` int(11) NOT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_foods`
--

CREATE TABLE `tbl_foods` (
  `id_makanan` int(11) NOT NULL,
  `nama_makanan` varchar(150) NOT NULL,
  `kalori` int(11) NOT NULL,
  `protein` decimal(5,2) NOT NULL,
  `lemak` decimal(5,2) NOT NULL,
  `karbo` decimal(5,2) NOT NULL,
  `porsi` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_foods`
--

INSERT INTO `tbl_foods` (`id_makanan`, `nama_makanan`, `kalori`, `protein`, `lemak`, `karbo`, `porsi`) VALUES
(1, 'Nasi Putih', 175, 4.00, 0.50, 40.00, '100 gram'),
(2, 'Ayam Goreng', 260, 25.00, 15.00, 0.00, '1 potong'),
(3, 'Telur Rebus', 80, 6.00, 5.00, 1.00, '1 butir'),
(4, 'Tempe Goreng', 150, 10.00, 8.00, 10.00, '1 potong'),
(5, 'Tahu Goreng', 120, 8.00, 7.00, 6.00, '1 potong'),
(6, 'Ikan Bakar', 200, 22.00, 10.00, 0.00, '1 potong'),
(7, 'Dada Ayam Panggang', 165, 31.00, 3.50, 0.00, '100 gram'),
(8, 'Roti Gandum', 90, 4.00, 1.00, 18.00, '1 lembar'),
(9, 'Oatmeal', 150, 5.00, 3.00, 27.00, '1 mangkok'),
(10, 'Pisang', 105, 1.00, 0.40, 27.00, '1 buah'),
(11, 'Apel', 95, 0.50, 0.30, 25.00, '1 buah'),
(12, 'Salad Sayur', 80, 3.00, 2.00, 12.00, '1 mangkok'),
(13, 'Susu Rendah Lemak', 100, 8.00, 2.50, 12.00, '1 gelas'),
(14, 'Yogurt Plain', 110, 6.00, 4.00, 12.00, '1 cup'),
(15, 'Kentang Rebus', 160, 4.00, 0.20, 37.00, '1 buah'),
(16, 'Spaghetti', 220, 8.00, 1.00, 43.00, '1 porsi'),
(17, 'Daging Sapi Panggang', 250, 26.00, 17.00, 0.00, '100 gram'),
(18, 'Udang Rebus', 120, 23.00, 1.00, 1.00, '100 gram'),
(19, 'Jagung Rebus', 150, 5.00, 2.00, 32.00, '1 buah'),
(20, 'Smoothie Buah', 180, 3.00, 2.00, 40.00, '1 gelas');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_olahraga`
--

CREATE TABLE `tbl_olahraga` (
  `id_olahraga` int(11) NOT NULL,
  `nama_olahraga` varchar(100) NOT NULL,
  `kalori_per_menit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_olahraga`
--

INSERT INTO `tbl_olahraga` (`id_olahraga`, `nama_olahraga`, `kalori_per_menit`) VALUES
(1, 'Jalan Santai', 4),
(2, 'Jalan Cepat', 6),
(3, 'Jogging', 8),
(4, 'Lari', 10),
(5, 'Bersepeda Santai', 7),
(6, 'Bersepeda Cepat', 12),
(7, 'Skipping', 11),
(8, 'Berenang', 9),
(9, 'Aerobik', 8),
(10, 'Zumba', 9),
(11, 'Yoga', 4),
(12, 'Pilates', 5),
(13, 'Push Up', 7),
(14, 'Sit Up', 6),
(15, 'Squat', 7),
(16, 'Angkat Beban', 6),
(17, 'Basket', 8),
(18, 'Futsal', 9),
(19, 'Badminton', 7),
(20, 'Naik Tangga', 10);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_users`
--

CREATE TABLE `tbl_users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` enum('L','P') NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `tinggi_cm` int(11) NOT NULL,
  `berat_kg` decimal(5,2) NOT NULL,
  `tingkat_aktivitas` enum('rendah','sedang','tinggi') NOT NULL,
  `tujuan` enum('diet','jaga','naik') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_users`
--

INSERT INTO `tbl_users` (`id`, `name`, `email`, `password`, `gender`, `tanggal_lahir`, `tinggi_cm`, `berat_kg`, `tingkat_aktivitas`, `tujuan`, `created_at`) VALUES
(2, 'tes', 'tes@gmail.com', 'pbkdf2:sha256:1000000$xsxqTlVbTW1JenSR$ee49af3afb25588ff7384fed28d73d491db903e3336e7970a0e8f710ab04d872', 'L', '2026-02-09', 175, 100.00, 'rendah', '', '2026-02-09 04:20:39'),
(3, 'azka', 'azka@gmail.com', 'pbkdf2:sha256:1000000$iDH6y6jRTTFxFvvP$19f345b1e1ca75b95a5dfee4c0bc2eba706a563042ce387e77ea6719f7ef1a4c', 'L', '2026-02-10', 176, 56.00, 'rendah', 'naik', '2026-02-10 11:56:21');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_user_targets`
--

CREATE TABLE `tbl_user_targets` (
  `id_target` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `target_kalori` int(11) NOT NULL,
  `target_protein` int(11) NOT NULL,
  `target_lemak` int(11) NOT NULL,
  `target_karbo` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_user_targets`
--

INSERT INTO `tbl_user_targets` (`id_target`, `user_id`, `target_kalori`, `target_protein`, `target_lemak`, `target_karbo`, `updated_at`) VALUES
(2, 2, 2699, 202, 90, 270, '2026-02-09 04:20:39'),
(3, 3, 2789, 209, 93, 279, '2026-02-10 11:56:21'),
(4, 2, 3258, 244, 109, 326, '2026-02-10 12:43:01'),
(5, 2, 2699, 202, 90, 270, '2026-02-10 12:43:06'),
(6, 2, 2886, 216, 96, 289, '2026-02-10 15:01:47');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tbl_catatan_air`
--
ALTER TABLE `tbl_catatan_air`
  ADD PRIMARY KEY (`id_catatan`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_tanggal` (`tanggal`);

--
-- Indeks untuk tabel `tbl_catatan_berat`
--
ALTER TABLE `tbl_catatan_berat`
  ADD PRIMARY KEY (`id_catatan`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_tanggal` (`tanggal`);

--
-- Indeks untuk tabel `tbl_catatan_makan`
--
ALTER TABLE `tbl_catatan_makan`
  ADD PRIMARY KEY (`id_catatan`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `id_makanan` (`id_makanan`),
  ADD KEY `idx_tanggal` (`tanggal`);

--
-- Indeks untuk tabel `tbl_catatan_olahraga`
--
ALTER TABLE `tbl_catatan_olahraga`
  ADD PRIMARY KEY (`id_catatan`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `id_olahraga` (`id_olahraga`),
  ADD KEY `idx_tanggal` (`tanggal`);

--
-- Indeks untuk tabel `tbl_foods`
--
ALTER TABLE `tbl_foods`
  ADD PRIMARY KEY (`id_makanan`);

--
-- Indeks untuk tabel `tbl_olahraga`
--
ALTER TABLE `tbl_olahraga`
  ADD PRIMARY KEY (`id_olahraga`);

--
-- Indeks untuk tabel `tbl_users`
--
ALTER TABLE `tbl_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indeks untuk tabel `tbl_user_targets`
--
ALTER TABLE `tbl_user_targets`
  ADD PRIMARY KEY (`id_target`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tbl_catatan_air`
--
ALTER TABLE `tbl_catatan_air`
  MODIFY `id_catatan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `tbl_catatan_berat`
--
ALTER TABLE `tbl_catatan_berat`
  MODIFY `id_catatan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `tbl_catatan_makan`
--
ALTER TABLE `tbl_catatan_makan`
  MODIFY `id_catatan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `tbl_catatan_olahraga`
--
ALTER TABLE `tbl_catatan_olahraga`
  MODIFY `id_catatan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `tbl_foods`
--
ALTER TABLE `tbl_foods`
  MODIFY `id_makanan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT untuk tabel `tbl_olahraga`
--
ALTER TABLE `tbl_olahraga`
  MODIFY `id_olahraga` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT untuk tabel `tbl_users`
--
ALTER TABLE `tbl_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `tbl_user_targets`
--
ALTER TABLE `tbl_user_targets`
  MODIFY `id_target` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tbl_catatan_air`
--
ALTER TABLE `tbl_catatan_air`
  ADD CONSTRAINT `tbl_catatan_air_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tbl_catatan_berat`
--
ALTER TABLE `tbl_catatan_berat`
  ADD CONSTRAINT `tbl_catatan_berat_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tbl_catatan_makan`
--
ALTER TABLE `tbl_catatan_makan`
  ADD CONSTRAINT `tbl_catatan_makan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_catatan_makan_ibfk_2` FOREIGN KEY (`id_makanan`) REFERENCES `tbl_foods` (`id_makanan`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tbl_catatan_olahraga`
--
ALTER TABLE `tbl_catatan_olahraga`
  ADD CONSTRAINT `tbl_catatan_olahraga_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_catatan_olahraga_ibfk_2` FOREIGN KEY (`id_olahraga`) REFERENCES `tbl_olahraga` (`id_olahraga`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tbl_user_targets`
--
ALTER TABLE `tbl_user_targets`
  ADD CONSTRAINT `tbl_user_targets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
