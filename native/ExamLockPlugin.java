package com.sk.successkit;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * Exam lock = Android "screen pinning". While a mock test with "auto submit" is running, the home / recents
 * swipe and the navigation bar stop working, so the test cannot be left by accident.
 * Android asks the student to confirm once ("Got it"), and the pin can always be removed by the
 * system gesture (touch and hold Back + Overview, or swipe up and hold).
 */
@CapacitorPlugin(name = "ExamLock")
public class ExamLockPlugin extends Plugin {

    @PluginMethod
    public void start(PluginCall call) {
        final Activity a = getActivity();
        if (a == null) { call.reject("no activity"); return; }
        a.runOnUiThread(() -> {
            try {
                a.startLockTask();
                call.resolve();
            } catch (Throwable t) {
                call.reject("lock fail: " + t.getMessage());
            }
        });
    }

    @PluginMethod
    public void stop(PluginCall call) {
        final Activity a = getActivity();
        if (a == null) { call.resolve(); return; }
        a.runOnUiThread(() -> {
            try {
                a.stopLockTask();
            } catch (Throwable ignored) {
                // not pinned right now - nothing to do
            }
            call.resolve();
        });
    }

    @PluginMethod
    public void state(PluginCall call) {
        JSObject r = new JSObject();
        boolean locked = false;
        try {
            ActivityManager am = (ActivityManager) getContext().getSystemService(Context.ACTIVITY_SERVICE);
            locked = am != null && am.getLockTaskModeState() != ActivityManager.LOCK_TASK_MODE_NONE;
        } catch (Throwable ignored) {
        }
        r.put("locked", locked);
        call.resolve(r);
    }
}
