use image::{DynamicImage, ImageFormat, Rgba};
use imageproc::{drawing::draw_text, drawing::text_size};
use lazy_static::lazy_static;
use pyo3::{prelude::*, types::PyByteArray};
use rusttype::{Font, Scale};
use std::io::Read;
use std::sync::Arc;
use std::time::Instant;
use std::{fs::File, io::Cursor, path::Path};

lazy_static! {
    static ref FONT: Font<'static> = load_font();
}
lazy_static! {
    static ref TEMPLATE_IMG: Arc<DynamicImage> = Arc::new(load_image_f());
}

// TODO: https://stackoverflow.com/questions/66241394/performant-method-of-drawing-text-onto-a-png-file
const COLOR: Rgba<u8> = Rgba([255, 255, 255, 255]);
const FONT_SIZE: f32 = 51f32;
const SCALE: Scale = Scale {
    x: FONT_SIZE,
    y: FONT_SIZE,
};

fn load_image_f() -> DynamicImage {
    if let Ok(image) = image::io::Reader::open("./static/template.png")
        .unwrap()
        .decode()
    {
        return image;
    }

    DynamicImage::default()
}

fn calculate_position(text: &str) -> i32 {
    // w595
    let ts = text_size(SCALE, &FONT, text).0;
    let pos = (595 - ts) / 2;
    pos
}

fn load_font() -> Font<'static> {
    let font_path = Path::new("./static/font.ttf");
    let mut font_data: Vec<u8> = Vec::new();
    File::open(font_path)
        .unwrap()
        .read_to_end(&mut font_data)
        .unwrap();
    Font::try_from_vec(font_data).unwrap()
}

#[pyfunction]
fn draw_on<'a>(py: Python<'a>, text: &'a str) -> &'a PyByteArray {
    let start = Instant::now();
    // img: Vec<u8>,
    let drewn = draw_text(
        TEMPLATE_IMG.as_ref(), // TEMPLATE_IMG: Arc<DynamicImage>
        COLOR,
        calculate_position(text),
        612,
        SCALE,
        &FONT,
        text,
    );
    let elapsed = start.elapsed();

    println!("Took {} ms. to manipulate the image", elapsed.as_millis());

    let mut pngbuf: Cursor<Vec<u8>> = Cursor::new(Vec::new());
    drewn.write_to(&mut pngbuf, ImageFormat::Png).unwrap();
    PyByteArray::new(py, &pngbuf.into_inner())
    //PyBytes::new(py, &pngbuf.into_inner())
}

#[pymodule]
fn barelimg(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(draw_on, m)?)?;
    Ok(())
}
