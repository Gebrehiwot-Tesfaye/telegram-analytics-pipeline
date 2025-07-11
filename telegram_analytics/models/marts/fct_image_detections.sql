select
    cast(message_id as bigint) as message_id,
    media_path,
    detected_object_class,
    confidence_score
from {{ source('public', 'image_detections') }}