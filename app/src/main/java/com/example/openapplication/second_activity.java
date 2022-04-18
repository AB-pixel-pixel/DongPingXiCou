package com.example.openapplication;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.ContentUris;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.nfc.Tag;
import android.os.Build;
import android.os.Bundle;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class second_activity extends AppCompatActivity {


    private ImageView picture;
    private Button chooseFromAlbum;


    public static final int CHOOSE_PHOTO=2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        picture = (ImageView) findViewById(R.id.imageView4);
        chooseFromAlbum = (Button) findViewById(R.id.button2);

        chooseFromAlbum.setOnClickListener(view -> {

           if(ContextCompat.checkSelfPermission(second_activity.this,
                   Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED)
           {
               ActivityCompat.requestPermissions(second_activity.this,new
                       String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},1);
           }
           else
           {
               openAlbum();
           }
        });
    }

    private void  openAlbum(){
        Intent intent=new Intent("android.intent.action.GET_CONTENT");
        intent.setType("image/*");
        startActivityForResult(intent,CHOOSE_PHOTO);

        /*String actionImageCapture = MediaStore.ACTION_IMAGE_CAPTURE;
        Intent intent=new Intent(actionImageCapture);
        intent.setType("image/*");
        registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), new ActivityResultCallback<ActivityResult>() {
            @Override
            public void onActivityResult(ActivityResult result) {

            }
        });*/


    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        requestCode=1;
        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                openAlbum();
            } else {
                Toast.makeText(this, "You denied the permission", Toast.LENGTH_SHORT).show();
            }
        }

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        super.onActivityResult(requestCode, resultCode, data);
        if (data == null){
            return;
        } else {
            if (requestCode == CHOOSE_PHOTO){
                handleImageOnKitKat(data);
            }
        }
    }


    private void handleImageBeforeKitKat(Intent data)
    {
        Uri uri = data.getData();
        String imagePath = getImagePath(uri,null);
        Toast.makeText(this,"fail to get image",Toast.LENGTH_SHORT).show();
        displayImage(imagePath);

    }


    private void handleImageOnKitKat(Intent data){

        String imagePath = null;
        Uri uri =data.getData();
        if(DocumentsContract.isDocumentUri(this,uri)){

//            "com.android.providers.media.documents".equals(uri.getAuthority())
//            "com.android.providers.downloads.documents".equals(uri.getAuthority())
            String docId =DocumentsContract.getDocumentId(uri);
            if(TextUtils.equals(uri.getAuthority(),"com.android.providers.media.documents")){


                String id = docId.split(":")[1];
                String selection = MediaStore.Images.Media._ID+"="+id;
                imagePath =getImagePath(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,selection);
                displayImage(imagePath);


            }else if(TextUtils.equals(uri.getAuthority(),"com.android.providers.downloads.documents")){
                if (docId != null && docId.startsWith("msf:")){
                    resolveMSFContent(uri,docId);
                    return;
                }
                Uri contentUri=ContentUris.withAppendedId(Uri.parse("content://downloads/public_downloads"),Long.valueOf(docId));
                imagePath = getImagePath(contentUri,null);
            }

        }else if("content".equalsIgnoreCase(uri.getScheme())){
            imagePath=getImagePath(uri,null);
        }else if("file".equalsIgnoreCase(uri.getScheme())) {
            imagePath = uri.getPath();
        }
        displayImage(imagePath);
    }

    private void resolveMSFContent(Uri uri, String documentId){
        File file = new File(getCacheDir(), "temp_file" + getContentResolver().getType(uri).split("/")[1]);
        Bitmap bitmap;
        try{
            InputStream inputStream = getContentResolver().openInputStream(uri);
            OutputStream outputStream = new FileOutputStream(file);
            byte[] buffer = new byte[4 * 1024];
            int read;
            while ((read = inputStream.read(buffer)) != -1){
                outputStream.write(buffer,0,read);
            }
            outputStream.flush();

            bitmap = BitmapFactory.decodeFile(file.getAbsolutePath());
            picture.setImageBitmap(bitmap);
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }
    }



    @SuppressLint("Range")
        private String getImagePath(Uri uri, String selection){
            String path = null;
            Cursor cursor = getContentResolver().query(uri,null,selection,null,null);
            if(cursor!=null){
                if(cursor.moveToFirst()) {
                    path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
                }
                cursor.close();
            }
            return path;
        }

    private void displayImage(String imagePath){

        if(imagePath!=null){
            Bitmap bitmap = BitmapFactory.decodeFile(imagePath);
            picture.setImageBitmap(bitmap);
        }
        else{
            Toast.makeText(this,"fail to get image",Toast.LENGTH_SHORT).show();
        }
    }

//    private boolean checkPermissions(){
//        final String[] ps = {Manifest.permission.READ_EXTERNAL_STORAGE};
//        int rc = ActivityCompat.checkSelfPermission(this, ps[0]);
//        if (rc != PackageManager.PERMISSION_GRANTED){
//            ActivityCompat.requestPermissions(this,ps,0);
//            return false;
//        }
//        return true;
//    }

}