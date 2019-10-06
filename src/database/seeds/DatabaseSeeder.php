<?php

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $this->call(CompanyInfoSeeder::class);
        $this->call(FinancialReportsSeeder::class);
        $this->call(CategoryInfoSeeder::class);
    }
}
