# 7z to zip_converter

This utility is created to convert 7z archive into ordinary zip archive with
which it is possible to work using Python's zipfile module without unarchiving. 
The difference of this util from other tools is that it extracts and 
zips files from archive one by one. Other tools like 'atoo' at first extract 
everything in a separate temporary folder and then archive everything in the
folder to zip archive. This behaviour is not desirable in case if extracted data
occupies a lot of space.

This utility has been created for Kaggle's competition "Microsoft Malware 
Classification Challenge (BIG 2015)".

To run this utility you must have 7z installed.

The work has been verified on Kubuntu 14.04 with Python 2.7 installed.

The command syntax:
// Instantiate the RequestQueue.
val queue = Volley.newRequestQueue(this)
val url = "https://meme-api.herokuapp.com/gimme"

// Request a string response from the provided URL.
val jsonObjectRequest = JsonObjectRequest(
        Request.Method.GET, url,null,
        Response.Listener { response ->
            val url = response.getString("url")
            Glide.with(this).load(url).into(imageview)

        },
        Response.ErrorListener { Toast.makeText(this,"Something went wrong",Toast.LENGTH_LONG).show() })

// Add the request to the RequestQueue.
queue.add(stringRequest)











android.permission.INTERNET




Or use Gradle:

repositories {
  google()
  jcenter()
}

dependencies {
  implementation 'com.github.bumptech.glide:glide:4.11.0'
  annotationProcessor 'com.github.bumptech.glide:compiler:4.11.0'
}





Glide.with(this).load(url).into(imageview)





```
python convert.py -jN <input_7z_file> <output_zip_file> 
```

Where N is the number of threads used to extract data. Usually, it is equal to
the number of threads that your processor is able to process simultaneously, 
e.g., if you have an Intel processor with 2 cores and enabled Hyperthreading
technology, N is equal to 4.
