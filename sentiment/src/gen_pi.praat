form Read all files of the given type from the given directory
   sentence Source_directory /Users/nibir/dev/544nlp/sentiment/data/youtube/corpus/audio/
   sentence Desti_directory /Users/nibir/dev/544nlp/sentiment/data/youtube/_praat/
   sentence File_extension .wav
endform

Create Strings as file list... list 'source_directory$'*'file_extension$'
head_words = selected("Strings")
file_count = Get number of strings

for current_file from 1 to file_count
   	select Strings list
   	filename$ = Get string... current_file
	filedelete 'Desti_directory$''filename$'.csv

	Read from file... 'source_directory$''filename$'
	sound = selected ("Sound")
	tmin = do ("Get start time")
	tmax = do ("Get end time")

	do ("To Pitch...", 0.01, 25, 300)
	do ("Rename...", "pitch")
	select sound
	do ("To Intensity...", 75, 0.01)
	do ("Rename...", "intensity")
	
	for i to (tmax-tmin)/0.01
	    time = tmin + i * 0.01
	    select Pitch pitch
	    pitch = do ("Get value at time...", time, "Hertz", "Linear")
	    if pitch = undefined
		pitch = 0
	    endif
	    select Intensity intensity
	    intensity = do ("Get value at time...", time, "Cubic")
	    if intensity = undefined
		intensity = 0
	    endif
	    fileappend 'Desti_directory$''filename$'.csv 'time:2','pitch:3','intensity:3''newline$'
	endfor
	
	select all
	minus Strings list
	Remove
	select Strings list
endfor

select all
Remove
clearinfo
echo Done! 'file_count' files read.'newline$'.