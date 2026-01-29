package com.eurobakshish.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.eurobakshish.ui.dashboard.DashboardActivity
import com.eurobakshish.ui.login.LoginActivity
import com.eurobakshish.utils.PreferenceManager

/**
 * Main activity - entry point of the application
 */
class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Check if user is logged in
        val preferenceManager = PreferenceManager(this)
        val intent = if (preferenceManager.isLoggedIn()) {
            Intent(this, DashboardActivity::class.java)
        } else {
            Intent(this, LoginActivity::class.java)
        }
        
        startActivity(intent)
        finish()
    }
}
