package com.example.imageviewer;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.content.Context;

public class MainActivity extends AppCompatActivity {
    Button button1;
    CheckBox checkBox1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(new MyGraphicView(this));
    }

    private static class MyGraphicView extends View {
        public MyGraphicView(Context context) {
            super(context);
        }
        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            // Bitmap picture = BitmapFactory.decodeResource(getResources(), R.drawable.image);
            Bitmap picture = BitmapFactory.decodeFile("/sdcard/DCIM/image.jpg");
            int picX = (this.getWidth() - picture.getWidth());
            int picY = (this.getHeight() - picture.getHeight());
            canvas.drawBitmap(picture, picX, picY, null);
            picture.recycle();
        }
    }
}