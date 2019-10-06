<?php

use Illuminate\Database\Seeder;

class CompanyInfoSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $file = new SplFileObject('database/csv_db/company_info_table.csv');
        $file->setFlags(
            \SplFileObject::READ_CSV |
                \SplFileObject::READ_AHEAD |
                \SplFileObject::SKIP_EMPTY |
                \SplFileObject::DROP_NEW_LINE
        );
        $list = [];
        $date = new DateTime();
        $now = $date->format('Y-m-d');
        foreach ($file as $line) {
            // var_dump(intval($line[8]));
            $list[] = [
                "edinet_code" => $line[0],
                "listing_category" => $line[1],
                "closing_date" => $line[2],
                "name" => $line[3],
                "name_en" => $line[4],
                "name_kana" => $line[5],
                "business_category" => intval($line[6]),
                "stock_code" => intval($line[7]),
                "company_id" => intval($line[8]),
                "created_at" => $now,
                "updated_at" => $now
            ];
        }

        $chunk_size = 1000;
        $chunk_data = array_chunk($list, $chunk_size);

        foreach ($chunk_data as $data) {
            DB::table("company_infos")->insert($data);
        }
    }
}
