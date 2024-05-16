# Function to aggressively clean non-quoted sections while preserving quoted values
import re

json_string = '{\n   "score": "85%",\n"reason": "The paper presents a detailed study on the development and implementation of a gamification-based learning platform in vocational education, directly related to your research topic.",\n"notes": "- The paper could benefit from further exploration of long-term impact on student motivation and engagement.\n- It would be useful to include comparisons with other gamification approaches in education for a more comprehensive analysis.",\n"added value": "This paper provides valuable insights into the effectiveness of gamification in improving student learning motivation in vocational education."\n}'


# Split at double quotes to isolate quoted content from non-quoted sections
parts = json_string.split('"')  # Split into non-quoted and quoted parts

# Clean non-quoted sections to remove control characters, excess spaces, and newlines
for i in range(len(parts)):
    print (i)
    if i % 2 == 0:  # Non-quoted sections
        # Remove all control characters and extra spaces
        parts[i] = re.sub(r'[\x00-\x1F\x7F]+', '', parts[i])  # Remove control characters
        parts[i] = parts[i].strip()

# Reconstruct the JSON structure by joining the parts with double quotes
cleaned_json_str = '"'.join(parts)  # Rejoin parts with double quotes

print(cleaned_json_str)



