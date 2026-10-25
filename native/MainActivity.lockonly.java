package com.sk.successkit;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

/** Used only when the build with the Gemma plugin fails: keeps the exam lock, drops Gemma. */
public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(ExamLockPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
