use pyo3::{prelude::*, types::PyByteArray};
use std::{io::Cursor, path::Path, fs::File};
use image::{ImageFormat, DynamicImage, Rgba};
use imageproc::{drawing::draw_text, drawing::text_size};
use rusttype::{Font, Scale};
use std::io::Read;
use lazy_static::lazy_static;
use std::sync::Arc;


lazy_static! {
    static ref FONT: Font<'static> = load_font();
}
lazy_static! {
    static ref TEMPLATE_IMG: Arc<DynamicImage> = Arc::new(load_image_f());
}

const COLOR: Rgba<u8> = Rgba([255, 255, 255, 255]);
const FONT_SIZE: f32 = 51f32;
const SCALE: Scale = Scale{x: FONT_SIZE, y: FONT_SIZE};


fn load_image_f() -> DynamicImage {
    if let Ok(image) = image::io::Reader::open("template.png").unwrap().decode() {
        return image;
    }
    DynamicImage::default()
}

#[allow(dead_code)]
fn load_image(img: Vec<u8>) -> DynamicImage {
    if let Ok(image) = image::load_from_memory(&img) {
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
    let font_path = Path::new("./font.ttf");
    let mut font_data: Vec<u8> = Vec::new();
    File::open(font_path).unwrap().read_to_end(&mut font_data).unwrap();
    Font::try_from_vec(font_data).unwrap()
}

#[pyfunction]
fn draw_on<'a>(py: Python<'a>, text: &'a str) -> &'a PyByteArray {  // img: Vec<u8>, 
    let drewn = draw_text(
        TEMPLATE_IMG.as_ref(),  // TEMPLATE_IMG: Arc<DynamicImage>
        COLOR,
        calculate_position(text),
        612,
        SCALE,
        &FONT,
        text
    );

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
