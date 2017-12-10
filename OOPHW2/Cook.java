package com.company;

public class Cook implements CookInterface {

    public String MealName;
    public String CustomerName;


    public Cook(String MealName, String CustomerName) {

        this.MealName = MealName;
        this.CustomerName = CustomerName;



    }

    @Override
    public void makethefood() {
        System.out.println("Cook prepares " + MealName + " for "+ CustomerName);

    }
}
