<?php

use Illuminate\Database\Seeder;

class CategoryInfoSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {

        $file = new SplFileObject('database/csv_db/category_info_table.csv'); // databaseフォルダの直下にcsv_dbを作成してその中にいくつかのcsvを作成した。

        // これがCSVを読み込む処理。基本そのまま
        $file->setFlags(
            \SplFileObject::READ_CSV |
                \SplFileObject::READ_AHEAD |
                \SplFileObject::SKIP_EMPTY |
                \SplFileObject::DROP_NEW_LINE
        );

        $list = [];
        $date = new DateTime();
        $now = $date->format('Y-m-d');
        // この中にCSVのデータとテーブルのカラム名を紐付ける
        foreach ($file as $line) {
            $list[] = [
                // "カラム名" => $line[x]  // x は カラムに入れるデータがcsvの何列目か指定
                "business_category" => intval($line[0]),
                // "business_category" => floatval($line[0], 6,3),float型で指定することもできる
                "business_category_name" => $line[1],
                "created_at" => $now,
                "updated_at" => $now
            ];
        }
        // DB::table("category_infos")->insert($data); // データの規模が大きくなければそのまま$dataを突っ込んでいい

        // データが巨大な場合は配列を分割して挿入していく
        $chunk_size = 1000;
        $chunk_data = array_chunk($list, $chunk_size);

        foreach ($chunk_data as $data) {
            DB::table("category_infos")->insert($data);
        }
        //ここまで
    }
}
