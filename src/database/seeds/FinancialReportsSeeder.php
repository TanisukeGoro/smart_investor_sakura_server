<?php

use Illuminate\Database\Seeder;

class FinancialReportsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $file = new SplFileObject('database/csv_db/master_financial_report_duplicates.csv');
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
            //
            // var_dump(floatval($line[14]));
            // var_dump('---');
            $list[] = [
                "Bonds" => floatval($line[1]),
                "CP" => floatval($line[2]),
                "Capex" => floatval($line[3]),
                "CashEquivalents" => floatval($line[4]),
                "Depreciation" => floatval($line[5]),
                "GrossProfit" => floatval($line[6]),
                "Inventories" => floatval($line[7]),
                "NetAssets" => floatval($line[8]),
                "NetSales" => floatval($line[9]),
                "OperatingProfit" => floatval($line[10]),
                "OrdinaryIncomeLoss" => floatval($line[11]),
                "ParseFlg" => floatval($line[12]),
                "ProfitLoss" => floatval($line[13]),
                "ROE" => floatval($line[14]),
                "RequestFlg" => floatval($line[15]),
                "ShareholdersEquity" => floatval($line[16]),
                "Valuation" => floatval($line[17]),
                "acPayable" => floatval($line[18]),
                "acReceivable" => floatval($line[19]),
                "cfFinancing" => floatval($line[21]),
                "cfInvesting" => floatval($line[22]),
                "cfOperating" => floatval($line[23]),
                "cpBonds" => floatval($line[24]),
                "cpLoans" => floatval($line[25]),
                "disclosureStatusFlg" => floatval($line[26]),
                "docID" => $line[27],
                "edinetCode" => $line[28],
                "filerName" => $line[29],
                "ltLoans" => floatval($line[30]),
                "psBasicEarningsLoss" => floatval($line[31]),
                "psNetAssets" => floatval($line[32]),
                "season" => floatval($line[33]),
                "series_data" => floatval($line[34]),
                "stBonds" => floatval($line[35]),
                "stLoans" => floatval($line[36]),
                "tAssets" => floatval($line[37]),
                "tIssuedShares" => floatval($line[38]),
                "xbrlFlg" => floatval($line[39]),
                "year" => floatval($line[40]),
                "created_at" => $now,
                "updated_at" => $now
            ];
        }
        $chunk_size = 1000;
        $chunk_data = array_chunk($list, $chunk_size);
        foreach ($chunk_data as $data) {
            DB::table("financial_reports")->insert($data);
        }
    }
}
